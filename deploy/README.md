# Deploying FindWine to Amazon EC2

## Setup server on EC2 (Ubuntu 16.04 LTS)

Do this on Amazon's management console.
Login using the instructions provided.

## Install dependencies

First run `sudo apt-get update`, then install:

- Python3 (should be installed)
- Pip: `sudo apt install python3-pip`
- Virtualenv: `pip3 install virtualenv`
- Virtualenvwrapper: `sudo pip3 install virtualenvwrapper`
- Mysql (MariaDB) client: `sudo apt install libmysqlclient-dev mariadb-client-10.0`

(There are other `apt` dependencies like supervisor and nginx, but these are pulled out into the relevant subsections)

## Setup user

```bash
$ sudo adduser findwine  # create account by following prompts
$ sudo usermod -aG sudo findwine  # give sudo access
# test it worked
$ sudo su findwine
$ sudo ls -la /root
```

## Setup directories

Make sure you are user `findwine` for this part.
```bash
$ cd /home/findwine
$ mkdir -p www/findwine && cd www/findwine
$ mkdir log
```

## Setup code root

First you need to setup deploy keys following [these instructions](https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys)

Then clone the repo into `code_root`
```bash
$ git clone git@github.com:FindWine/findwine.git code_root
```

*Note: if the above command fails it's likely because the deploy keys were not setup correctly).*

## Setup virtualenv

```bash
mkvirtualenv -p /usr/bin/python3  --no-site-packages findwine
```

If `mkvirtualenv` isn't found, you may need to follow [these instructions](https://stackoverflow.com/a/13855464/8207) to get it working.

If that completed successfuly you should now be in the virtualenv, which you can verify as per belwow:

```bash
$ which python
/home/findwine/.virtualenvs/findwine/bin/python
```

## Setup python packages

```bash
cd code_root
pip install -r requirements/requirements.txt
```

## Setup localsettings

```bash
touch findwine/localsettings.py
```

Then edit with production settings.

You will want to start with the defaults that include database and staticfiles info from other instances.

You will also need to set `ALLOWED_HOSTS` to support whatever DNS you are using.

## Setup database

TODO: this is currently not documented since the legacy database is being used.

To grant access to the existing database from the new server, just edit the security policy in the
[EC2 Management Console](https://eu-west-1.console.aws.amazon.com/ec2/v2/home?region=eu-west-1#SecurityGroups:sort=groupId).

## Test

At this point you can run a quick test to see whether things are working:

```
./manage.py runserver 0.0.0.0:8000
curl localhost:8000
```

Hopefully curl will return a real page and not an error page.
If you have already setup `ALLOWED_HOSTS` you should also now be able to view the site in a browser at:
http://www.findwine.com:8000/ (or whatever URL you have).

## Install gunicorn

```bash
$ pip install -r requirements/prod-requirements.txt
```

Again you can test by running something like the below with curl or in a browser:

```bash
$ gunicorn -w 4 -b 0.0.0.0:8000 findwine.wsgi
```

# Automating Processes with Supervisord

First install Supervisord: `sudo apt install supervisor`

## Setup supervisor directory and files

```bash
mkdir -p ../services/supervisor/
cp deploy/files/findwine-supervisor.conf ../services/supervisor/
```
Then edit the root `supervisor.conf` file.

```
sudo emacs /etc/supervisor/supervisord.conf
```

By adding this to the last line of the according to the directory above: `/home/findwine/www/findwine/services/supervisor/*.conf`

Then reload supervisor and confirm working by checking the status:

```bash
$ sudo supervisorctl reload
$ sudo supervisorctl status
````

The last command should show something like `findwine-django                  RUNNING   pid 14270, uptime 0:00:02` if it is running.

# Setup nginx as the web server

First you need to install Nginx:

```bash
sudo apt install nginx
```

And disable the default site:

```
sudo rm /etc/nginx/sites-enabled/default
```

Then setup the config files

```bash
sudo cp deploy/files/findwine-nginx.conf /etc/nginx/sites-available/findwine
sudo cp deploy/files/www-nginx.conf /etc/nginx/sites-available/www
```
And make them public:

```bash
sudo ln -s /etc/nginx/sites-available/findwine /etc/nginx/sites-enabled/findwine
sudo ln -s /etc/nginx/sites-available/www /etc/nginx/sites-enabled/www
```

Restart nginx

```bash
sudo service nginx reload
```

You should now be able to access the site on port 80 (no port specified): http://www.findwine.com/

# Setup SSL

## Setup cert

Instructions here: https://certbot.eff.org/#ubuntuxenial-nginx

First setup the directory
```
mkdir /var/www/ssl-proof/findwine/
```

Then update nginx config with the following lines and restart nginx

```
location /.well-known {
    root /var/www/ssl-proof/findwine/;
}
```

Then you can run the scripts

```
certbot certonly
```

Follow instructions pointing at the /var/www/ssl-proof/findwine/ directory

It will generate some files - pay attention to where they are and then update
/etc/nginx/sites-available/www accordingly to finalize setup

Example Output:
```
/etc/letsencrypt/live/www.findwine.com/fullchain.pem
Generating key (2048 bits): /etc/letsencrypt/keys/0001_key-certbot.pem
Creating CSR: /etc/letsencrypt/csr/0001_csr-certbot.pem
```

more info here: http://tom.busby.ninja/letsecnrypt-nginx-reverse-proxy-no-downtime/

## Renewal

check sudo crontab -e and make sure renewals are setup

# Taking Database dumps and restoring them locally for development

From the findwine.com server, take mysql dump:

```bash
mysqldump -h findwinemariadbinstance2.ctlfpxz1vplj.eu-west-1.rds.amazonaws.com -P 3306 -u lucienrawden -p findwinedb > ~/findwine.sql
```

Get file locally:

```bash
scp findwine@findwine.com:findwine.sql ./
```

Restore locally:
```bash
mysql -u root -p findwine < findwine.sql
```

# Setup remote login

Add your public key to `/home/findwine/.ssh/authorized_keys` to setup passwordless ssh access.

Test using:

```bash
$ ssh findwine@findwine.com
```

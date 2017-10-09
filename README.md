Find Wine Source Code
---------------------
A wine listing and review site built in Django.

# Installation

## Prerequisites

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python 3](https://www.python.org/downloads/)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)
- [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
- [MySQL](https://dev.mysql.com/downloads/) (for production data)
- [MySQL](https://dev.mysql.com/downloads/) (for production data)

## Clone repository

You may need to setup your [github SSH keys](https://help.github.com/articles/connecting-to-github-with-ssh/) to clone without entering a password.

To clone with SSH use:

`git@github.com:FindWine/findwine.git`

Alternatively use HTTPS:

`git clone https://github.com/FindWine/findwine.git`

## Setup Virtualenv

`mkvirtualenv --no-site-packages findwine -p python3`

## Install requirements:

Make sure you are in the root directory of the `findwine` repository (`cd findwine`) then run:

`pip install -r requirements/requirements.txt`

## Setup database

### Empty Database

If you just want an empty database you can run:

`./manage.py migrate`

which will create a SQLite database file and initialize the necessary tables.

### Production Database

If you want access to the production database do the following:

First download the `findwine-db.sql` and `settings_production.py` files from [Dropbox](https://www.dropbox.com/home/AWS/Passwords%20etc).

#### Create a MySQL database

```bash
$ mysql -u root -p   # get a mysql shell. enter password (and change username if needed)
> create database findwine;
```

#### Dump the data into the newly created DB

```bash
$ mysql -u root -p findwine < findwine-db.sql
```

#### Update your localsettings to point to the new database

First move the downloaded `settings_production.py` file into the `findwine` folder (where `settings.py` is).

Next create a `localsettings.py` file:

```bash
cp findwine/localsettings.example.py findwine/localsettings.py
```

Edit the file with your MySQL user/password as needed.

#### Run server

Finally you can run the server:

```bash
./manage.py runserver
```

And your server should be running at http://localhost:8000/

# Getting Updates

To get the latest version of the code running in a local environment you can run the following (requires installing fabric):

First make sure you are in the virtualenv:

```bash
workon findwine
```

Then:

```bash
fab update_local
./manage.py runserver
```

# Running Tests

To run tests, first make sure you have the dev requirements installed:

```bash
$ pip install -r requirements/dev-requirements.txt
```

Then run the following:

```bash
$ pip install -r requirements/dev-requirements.txt
```

```bash
$ ./manage.py test
```

You can also run subsets of the tests as needed:

```bash
# by module
$ ./manage.py test wine.tests.test_countries
# by test case
$ ./manage.py test wine.tests.test_countries:CountriesTest
# by test method
$ ./manage.py test wine.tests.test_countries:CountriesTest.test_all_choices
```

## Using Sniffer

It is highly recommended to use sniffer to run tests when doing active development.
Sniffer will automatically watch files for changes and rerun tests as needed.

To run sniffer just use the following:

```bash
$ sniffer -x -s ./manage.py -x wine.tests.test_countries
```

Like normal tests, you can use sniffer to run any subset of the tests using the same syntax as above.

# Production Setup/Install

See [deploy README](../deploy/README.md) for details on production setup / install.

# Deploying code to production

Make sure you have fabric installed:

```bash
$ pip install -r requirements/dev-requirements.txt
```

Then just run:

```bash
$ fab production deploy
```

You will need the password for the `findwine` user on production.

# Building requirements

Dependencies should be added to requirements.in and then compiled to requirements.txt.

To do this, first install pip-tools:

`pip install pip-tools`

Then run:

`pip-compile --output-file requirements/requirements.txt requirements/requirements.in`

# Frond end setup

React instructions largely from [the installation docs](https://reactjs.org/docs/installation.html).

Note this is just during bootstrap.

```bash
yarn init
yarn add react react-dom
yarn add webpack --dev
yarn add babel-core babel-cli babel-loader babel-preset-react babel-preset-env babel-preset-es2015 --dev
```

## Building Front end

Watch for changes in develop mode:

`./node_modules/webpack/bin/webpack.js --watch`


Build for production:

`./node_modules/webpack/bin/webpack.js --watch --optimize-minimize -p`

# Todos

The main roadmap for this project is kept [on Trello](https://trello.com/b/wDRdlcjU/findwine-dev).

Here are a few code todos:

- Better handling of static files
- Remove inline style declarations

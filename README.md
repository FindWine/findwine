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

# Production Setup/Install

See [deploy README](../deploy/README.md) for details on production setup / install.

# Building requirements

Dependencies should be added to requirements.in and then compiled to requirements.txt.

To do this, first install pip-tools:

`pip install pip-tools`

Then run:

`pip-compile --output-file requirements/requirements.txt requirements/requirements.in`

# Todos

The main roadmap for this project is kept [on Trello](https://trello.com/b/wDRdlcjU/findwine-dev).

Here are a few code todos:

- Static files

Find Wine Source Code
---------------------
A wine listing and review site built in Django.

# Installation

## Prerequisites

- [Python 3](https://www.python.org/downloads/)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)
- [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

## Setup Virtualenv

`mkvirtualenv --no-site-packages findwine -p python3`

## Install requirements:

`pip install -r requirements.txt`

## Setup local settings (optional):

`touch findwine/localsettings.py`

Edit the file as needed.

## Setup database

`./manage.py migrate`


# Production Setup/Install

## Install MySQL (MariaDB) client

`sudo apt-get install libmysqlclient-dev`

# Building requirements

Dependencies should be added to requirements.in and then compiled to requirements.txt.

To do this, first install pip-tools:

`pip install pip-tools`

Then run:

`pip-compile --output-file requirements.txt requirements.in`

# Todos

The main roadmap for this project is kept [on Trello](https://trello.com/b/wDRdlcjU/findwine-dev).

Here are a few code todos:

- Static files
- Document production settings

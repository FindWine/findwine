Find Wine Source Code
---------------------

# Installation

## Setup Virtualenv

`mkvirtualenv --no-site-packages findwine -p python3`

## Install requirements:

`pip install -r requirements.txt`

## Setup local settings (optional):

`touch findwine/localsettings.py`

Edit the file as needed.

## Setup database

`./manage.py migrate`


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
-

from .settings_production import *  # for production settings

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "findwine",
        "USER": "root",
        "PASSWORD": "*****",
        "HOST": "localhost",
    }
}

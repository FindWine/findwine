from .settings_production import *  # for production settings

ALLOWED_HOSTS = []

STATIC_URL = '/static/'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

SITE_URL = 'http://localhost:8000'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "findwine",
        "USER": "root",
        "PASSWORD": "*****",
        "HOST": "localhost",
    }
}

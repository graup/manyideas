# -*- coding: utf-8 -*-

from .common import *  # noqa

DEBUG = True
TESTING = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SECRET_KEY = 'foobarbaz'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

BASE_URL = 'http://localhost:8000'

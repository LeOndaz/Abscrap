from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'abscrap',
        'USER': 'scraptit',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

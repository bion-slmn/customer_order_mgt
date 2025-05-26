
from pathlib import Path
from .base import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SECRET_KEY = 'django-insecure-=%1@5%v7v^zgbafou-i6o180+8%s=e7rj($5tw93ma(m(=t6@m'

DEBUG = True


ALLOWED_HOSTS = []


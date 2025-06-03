from pathlib import Path
from .base import *
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = True


ALLOWED_HOSTS = ["my-python-app-1018047469031.europe-southwest1.run.app"]
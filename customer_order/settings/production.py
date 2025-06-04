from pathlib import Path
from .base import *
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.{}'.format(
             os.getenv('DATABASE_ENGINE', 'sqlite3')
         ),
         'NAME': os.getenv('DATABASE_NAME', 'customer_mgt'),
         'USER': os.getenv('DATABASE_USERNAME', 'myprojectuser'),
         'PASSWORD': os.getenv('DATABASE_PASSWORD', 'password'),
         'HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
         'PORT': os.getenv('DATABASE_PORT', 5432),
     }
 }

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = True


ALLOWED_HOSTS = ["my-python-app-1018047469031.europe-southwest1.run.app", "127.0.0.1", "localhost"]
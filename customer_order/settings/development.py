
from pathlib import Path
from .base import *
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.{}'.format(
             os.getenv('DATABASE_ENGINE', 'sqlite3')
         ),
         'NAME': os.getenv('DATABASE_NAME', 'polls'),
         'USER': os.getenv('DATABASE_USERNAME', 'myprojectuser'),
         'PASSWORD': os.getenv('DATABASE_PASSWORD', 'password'),
         'HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
         'PORT': os.getenv('DATABASE_PORT', 5432),
     }
 }

SECRET_KEY = 'django-insecure-=%1@5%v7v^zgbafou-i6o180+8%s=e7rj($5tw93ma(m(=t6@m'

DEBUG = True


ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS","localhost").split(",")


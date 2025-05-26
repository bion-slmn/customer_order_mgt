import os
from dotenv import load_dotenv

load_dotenv()


if os.getenv('DJANGO_ENV') == 'production':
    from .production import *
else:
    from .development import *
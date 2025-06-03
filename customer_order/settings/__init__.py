import os
from dotenv import load_dotenv

load_dotenv()


print(os.getenv('DJANGO_ENV'), 222222222222222222222222)

if os.getenv('DJANGO_ENV') == 'production':
    from .production import *
else:
    from .development import *
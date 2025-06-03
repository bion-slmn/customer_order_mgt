set -e

python manage.py makemigrations

# Run database migrations
python manage.py migrate --noinput

# Start the Gunicorn server
exec gunicorn --bind 0.0.0.0:$PORT customer_order.wsgi:application
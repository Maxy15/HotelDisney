set -e

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis started"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating admin user..."
python manage.py shell -c "from api.seeds import create_admin_user; create_admin_user()" || true

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# Ejecutar según el comando
if [ "$1" = "celery" ]; then
  echo "Starting Celery worker..."
  exec celery -A cts_backend worker --loglevel=info
elif [ "$1" = "server" ]; then
  echo "Starting Django server..."
  exec python manage.py runserver 0.0.0.0:8000
else
  exec "$@"
fi
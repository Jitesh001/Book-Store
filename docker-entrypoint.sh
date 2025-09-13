#!/bin/bash
set -euo pipefail

# Wait for DB if provided (compose service name "postgres")
if [[ -n "${DB_HOST:-}" ]]; then
  echo "Waiting for database at $DB_HOST:${DB_PORT:-5432}..."
  for i in {1..60}; do
    (echo > /dev/tcp/$DB_HOST/${DB_PORT:-5432}) >/dev/null 2>&1 && break
    sleep 1
    if [[ $i -eq 60 ]]; then
      echo "Database not reachable" >&2
      exit 1
    fi
  done
fi

# Migrations
echo "Applying database migrations"
python src/manage.py migrate --noinput

# # Collect static to STATIC_ROOT (set this in settings to /app/staticfiles)
# echo "Collecting static files"
python src/manage.py collectstatic --noinput

# Runserver (Gunicorn)
# Adjust module to your actual wsgi module. Commonly: src.wsgi:application
echo "Starting Gunicorn"
exec gunicorn src.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-60}

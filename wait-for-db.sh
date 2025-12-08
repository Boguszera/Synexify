#!/bin/sh
set -e

host="$DB_HOST"
export PGPASSWORD="$DB_PASSWORD"
shift
cmd="$@"

until psql -h "$host" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is up - executing migrations"

python manage.py makemigrations orm

python manage.py migrate --noinput

echo "Starting command: $cmd"
exec $cmd

#!/bin/sh

set -e

echo "Wait for database become available"
python manage.py wait_for_db
echo "Apply database migrations"
python manage.py migrate --noinput
echo "Rebuild Solr index"
python manage.py rebuild_index --noinput

exec "$@"
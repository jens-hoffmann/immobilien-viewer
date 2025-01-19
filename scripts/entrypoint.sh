#!/bin/sh

set -e

echo "Wait for database become available"
python manage.py wait_for_db
echo "Apply database migrations"
python manage.py migrate --noinput
echo "Import districts from geojson"
python manage.py import_geojson_districts
echo "Rebuild Solr index"
python manage.py rebuild_index --noinput

exec "$@"
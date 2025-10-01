#!/bin/sh
set -e

# Wait for MySQL to be available before running migrations
HOST=${MYSQL_HOST:-db}
PORT=${MYSQL_PORT:-3306}

python - <<'PY'
import os, time, sys
import MySQLdb

host = os.getenv('MYSQL_HOST', 'db')
port = int(os.getenv('MYSQL_PORT', '3306'))
user = os.getenv('MYSQL_USER', 'teatrope')
password = os.getenv('MYSQL_PASSWORD', 'teatrope')

max_attempts = 60
attempt = 0
while attempt < max_attempts:
    try:
        conn = MySQLdb.connect(host=host, port=port, user=user, passwd=password)
        conn.close()
        print("Database is available")
        sys.exit(0)
    except Exception as e:
        attempt += 1
        print(f"Waiting for database ({e})... attempt {attempt}/{max_attempts}", flush=True)
        time.sleep(2)

print("Database did not become available in time", flush=True)
sys.exit(1)
PY

python manage.py makemigrations accounts content discovery notifications tickets || true
python manage.py migrate --noinput || true

exec "$@"


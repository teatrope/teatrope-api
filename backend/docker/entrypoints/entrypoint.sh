#!/bin/sh
set -e

# Wait for MySQL to be available before running migrations
python - <<'PY'
import os, time, sys
from urllib.parse import urlparse
import MySQLdb

database_url = os.getenv('DATABASE_URL')
if not database_url:
    print("DATABASE_URL not set", flush=True)
    sys.exit(1)

parsed = urlparse(database_url)
host = parsed.hostname
port = int(parsed.port) if parsed.port else 3306
user = parsed.username
password = parsed.password
db_name = parsed.path.lstrip('/')

max_attempts = 60
attempt = 0
while attempt < max_attempts:
    try:
        conn = MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=db_name)
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
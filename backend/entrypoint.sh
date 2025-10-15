#!/bin/sh
set -e

python - <<'PY'
import os, time
import psycopg2

dsn = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST', 'db'),
    'port': int(os.getenv('POSTGRES_PORT', '5432')),
}
for _ in range(30):
    try:
        psycopg2.connect(**dsn).close()
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("DB is not available")
PY

alembic upgrade head

exec uvicorn app.main:app --host ${UVICORN_HOST:-0.0.0.0} --port ${UVICORN_PORT:-8000}

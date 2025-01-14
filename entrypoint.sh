#!/usr/bin/env bash

set -e

alembic revision --autogenerate -m "Increase password_hash length"
echo "Applying Alembic migrations..."
alembic upgrade head

echo "starting server..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000

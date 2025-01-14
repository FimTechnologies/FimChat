#!/usr/bin/env bash

set -e

echo "Applying Alembic migrations..."
alembic upgrade head || alembic revision --autogenerate -m "Recreating missing migration" && alembic upgrade head

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

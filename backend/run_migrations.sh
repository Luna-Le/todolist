#!/bin/sh

# Wait for the database to be ready
while ! nc -z postgres 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Run migrations
alembic upgrade head
#!/bin/bash

# Exit immediately on error
set -e

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
until pg_isready -h "$DB_HOST" -U "$POSTGRES_USER"; do
  sleep 1
done

# Run migrations and start server
python manage.py migrate
python manage.py runserver 0.0.0.0:8010

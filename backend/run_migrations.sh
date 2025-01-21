while ! nc -z postgres 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done


alembic upgrade head
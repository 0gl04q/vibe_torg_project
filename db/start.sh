#!/bin/bash
set -e

docker-entrypoint.sh postgres &

until pg_isready -h localhost -p 5432 -U "$POSTGRES_USER"; do
  echo "Waiting for Postgres to be ready..."
  sleep 2
done

./docker-entrypoint-initdb.d/db_init.sh

wait -n
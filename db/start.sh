#!/bin/bash
set -e

# Запускаем Postgres в фоновом режиме
docker-entrypoint.sh postgres &

# Ожидаем, пока Postgres полностью запустится
until pg_isready -h localhost -p 5432 -U "$POSTGRES_USER"; do
  echo "Waiting for Postgres to be ready..."
  sleep 2
done

# Запускаем наш скрипт инициализации
./docker-entrypoint-initdb.d/db_init.sh

# Даем контейнеру возможность продолжить работу
wait -n
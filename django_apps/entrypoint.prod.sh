#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Postgres еще не запущен"

  while  ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 10
  done

  echo "PostgreSQL запущен"
fi

exec "$@"
#!/bin/sh

COMMAND_CREATE_LENDING_POSTGRES_DB="CREATE DATABASE $LENDING_POSTGRES_DB;"

psql -h "$SQL_HOST" -p "$SQL_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "$COMMAND_CREATE_LENDING_POSTGRES_DB"
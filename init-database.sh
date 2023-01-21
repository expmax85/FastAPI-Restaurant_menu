#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$DB_USER" --dbname "$DB_NAME" <<-EOSQL
    CREATE DATABASE main_db;
    CREATE DATABASE test_db;
EOSQL
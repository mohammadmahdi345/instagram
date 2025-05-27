#!/bin/bash
# wait-for-db.sh

HOST=$1
shift
PORT=3306

until nc -z $HOST $PORT; do
  echo "Waiting for database at $HOST:$PORT..."
  sleep 2
done

echo "Database is up, running command..."
exec "$@"
#!/bin/bash

until alembic upgrade head
do
    echo "Waiting for db to be ready..."
    sleep 10
done
cd /usr/local/task_service/cmd
uvicorn main:app --reload --host 0.0.0.0 --port 11022
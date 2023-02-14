#!/usr/bin/env bash

docker build .
docker-compose build
docker-compose run --rm app sh -c "python manage.py makemigrations"
docker-compose run --rm app sh -c "python manage.py makemigrations books user"
docker-compose run --rm app sh -c "python manage.py migrate"

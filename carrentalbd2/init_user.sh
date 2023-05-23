#!/usr/bin/bash

export DJANGO_SUPERUSER_PASSWORD=$1
export DJANGO_SUPERUSER_USERNAME=$2
export DJANGO_SUPERUSER_EMAIL=$3

python3 ./manage.py createsuperuser --noinput

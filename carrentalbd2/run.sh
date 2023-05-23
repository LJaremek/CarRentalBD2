#!/usr/bin/bash

pg_ctl -D database -l logfile start

python3 ./manage.py runserver
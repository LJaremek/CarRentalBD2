#!/usr/bin/bash

sudo service postgresql start
sudo -u postgres psql -f init.sql
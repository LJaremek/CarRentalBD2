#!/usr/bin/bash

sudo apt install postgresql
sudo service postgresql start
sudo -u postgres psql -f init.sql
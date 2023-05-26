#!/usr/bin/bash

# initdb -D database
# pg_ctl -D database -l logfile start
# createuser --encrypted --pwprompt admin1
# createdb --owner=admin1 postgres_db

sudo apt-get install

git pull
sudo apt install postgresql
sudo apt install python3-pip
pip install -r requirements.txt

./init_db.sh postgres_db admin haslo1

python3 ./manage.py makemigrations
python3 ./manage.py migrate

./init_user.sh haslo1 admin admin@pw.pl

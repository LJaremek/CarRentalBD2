initdb -D database
pg_ctl -D database -l logfile start
createuser --encrypted --pwprompt admin1
createdb --owner=admin1 postgres_db

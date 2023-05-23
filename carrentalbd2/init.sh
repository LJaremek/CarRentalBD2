sudo apt-get install

git pull

sudo apt install python3-pip
pip install -r requirements.txt

python3 ./manage.py makemigrations
python3 ./manage.py migrate

python3 ./manage.py createsuperuser
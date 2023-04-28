# CarRentalBD2
Car Rental for Bazy Danych 2


## Instalacja wymaganych bibliotek
```
pip install -r requirements.txt
```

## Robienie migracji
```
python .\manage.py makemigrations carrental
python .\manage.py migrate
```
## Tworzenie admina
```
python .\manage.py createsuperuser
```

## Uruchomienie servera
```
python .\manage.py runserver
```
W przeglądarce wywołujemy http://localhost:8000/admin/. Podajemy dane logowani utworzonego w poprzednim punkcie superusera.



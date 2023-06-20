# CarRentalBD2
Car Rental for Bazy Danych 2

## Szybki start

### Zbudowanie repo
```
cd carrentalbd2
chmod +x ./init.sh
./init.sh
```

### Włączenie servera
```
chmod +x ./run.sh
./run.sh
```


## Instalacja wymaganych bibliotek
```
pip install -r requirements.txt
```

## Robienie migracji
```
python3 ./manage.py makemigrations
python3 ./manage.py migrate
```
## Tworzenie admina
```
python3 ./manage.py createsuperuser
```

## Uruchomienie servera
```
python3 ./manage.py runserver 0:8000
```
W przeglądarce wywołujemy http://localhost:8000/admin/. Podajemy dane logowani utworzonego w poprzednim punkcie superusera.

## Funkcjonalność aplikacyjna

Po zalogowaniu do interfejsu administratora ukazują nam się utworzone obiekty. Możemy je usuwać, dodawać i edytować.

## Funkcjonalność analityczno-raportowa

W interfejsie mamy możliwość generowania wybranych wykresów. Wyświetlamy je poprzez: Reports -> Wybrany_Raport -> add

## Procedury

Procedury znajdują się w [katalogu ./carrentalbd2/procedures/](./carrentalbd2/procedures/) 



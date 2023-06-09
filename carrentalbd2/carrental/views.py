from django.shortcuts import render, redirect
from .forms import MyForm, MyCompanyForm
from django.db import connection
from django.core.paginator import Paginator
from carrental.models import Client
from .models import Person, Company, Rental, Car
from django.utils import timezone

# Create your views here.


def my_account(request):
    # try person
    username = str(request.GET.get("login"))
    cancel_status = str(request.GET.get("cancel_status"))
    my_user_data = None
    query = ""
    user_data_dict = {}
    user_data = []
    my_user_data = []
    with connection.cursor() as cursor:
        with open("views/client_person.sql") as f:
            query = f.read()
            cursor.execute(query, [username])
            user_data = cursor.fetchall()
    if len(user_data) > 0:
        my_user_data = user_data[0]
        user_data_dict = {
            "first_name": my_user_data[4],
            "pesel": my_user_data[5],
            "surname": my_user_data[6],
        }
    else:
        with connection.cursor() as cursor:
            with open("views/client_company.sql") as f:
                query = f.read()
                cursor.execute(query, [username])
                user_data = cursor.fetchall()
        my_user_data = user_data[0]
        user_data_dict = {
            "name": my_user_data[4],
            "nip": my_user_data[5],
            "sector": my_user_data[6],
        }
    user_data_dict["country"] = my_user_data[0]
    user_data_dict["email"] = my_user_data[1]
    user_data_dict["login"] = my_user_data[2]
    user_data_dict["phone"] = my_user_data[3]

    with connection.cursor() as cursor:
        with open("views/users_rental.sql") as f:
            query = f.read()
            cursor.execute(query, [my_user_data[7]])
            rentals = cursor.fetchall()
    rentals_dicts = [
        {
            "model": rental[0],
            "plate": rental[1],
            "rental_id": rental[2],
            "start_date": rental[3],
            "car_id": rental[4]
        }
        for rental in rentals
    ]

    # for cancelling rentals:
    if cancel_status == "success":
        rent_id = str(request.GET.get("rental_id"))
        print(rent_id)
        with connection.cursor() as cursor:
            with open("views/cancel_rent.sql") as f:
                query = f.read()
                cursor.execute(query, [rent_id])

    with connection.cursor() as cursor:
        with open("views/user_rental_history.sql") as f:
            # select rental history - rentals with end date not null
            query = f.read()
            cursor.execute(query, [my_user_data[7]])
            rentals_history = cursor.fetchall()
    rentals_history_dict = [
        {
            "model": r_hist[0],
            "plate": r_hist[1],
            "rental_id": r_hist[2],
            "start_date": r_hist[3],
            "end_date": r_hist[4],
            "car_id": r_hist[5]
        }
        for r_hist in rentals_history
    ]


    context = {
        "user": user_data_dict,
        "rentals": rentals_dicts,
        "rentals_history": rentals_history_dict,
        "cancel_status": cancel_status
    }
    return render(request, "my_account.html", context)


def log_screen_view(request):
    # loading procedures and functions to database
    with open("procedures/registration.sql", "r") as sql_file:
        sql = sql_file.read()
    with connection.cursor() as cursor:
        cursor.execute(sql)
    with open("procedures/check_login.sql", "r") as sql_file:
        sql = sql_file.read()
    with connection.cursor() as cursor:
        cursor.execute(sql)
    # parsing text to the base/ page
    text_value = request.GET.get("text", "")
    return render(request, "base.html", {"text": text_value})


def registration_person(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            repeated_password = form.cleaned_data["repeated_password"]
            phone = form.cleaned_data["phone"]
            country = form.cleaned_data["country"]
            pesel = form.cleaned_data["pesel"]
            first_name = form.cleaned_data["first_name"]
            second_name = form.cleaned_data["second_name"]
            print(country)
            # Process the form data or save it to the database
            try:
                with connection.cursor() as cursor:
                    cursor.callproc(
                        "validate_input_data_person",
                        [
                            username,
                            email,
                            password,
                            repeated_password,
                            phone,
                            pesel,
                            first_name,
                            second_name,
                        ],
                    )
                    client = Client.objects.create(
                        login=username,
                        email=email,
                        password=password,
                        phone=phone,
                        country=country,
                    )
                    client.save()
                    person = Person.objects.create(
                        pesel=pesel,
                        first_name=first_name,
                        second_name=second_name,
                        parent=client,
                    )
                    person.save()
                    with connection.cursor() as cursor:
                        cursor.execute("CALL fix_bug_person_empty_record()")
            except Exception:
                return redirect("/base/?text={}".format("Unuccessful registration"))

            return redirect("/base/?text={}".format("Successful registration"))
    else:
        form = MyForm()
    return render(request, "client_registration.html", {"form": form})


def registration_company(request):
    if request.method == "POST":
        form = MyCompanyForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            repeated_password = form.cleaned_data["repeated_password"]
            phone = form.cleaned_data["phone"]
            country = form.cleaned_data["country"]
            nip = form.cleaned_data["nip"]
            name = form.cleaned_data["name"]
            sector = form.cleaned_data["sector"]
            print(country)
            # Process the form data or save it to the database
            try:
                with connection.cursor() as cursor:
                    cursor.callproc(
                        "validate_input_data_company",
                        [
                            username,
                            email,
                            password,
                            repeated_password,
                            phone,
                            nip,
                            name,
                            sector,
                        ],
                    )

                client = Client.objects.create(
                    login=username,
                    email=email,
                    password=password,
                    phone=phone,
                    country=country,
                )
                client.save()
                comapny = Company.objects.create(
                    nip=nip, name=name, sector=sector, parent=client
                )
                comapny.save()
                with connection.cursor() as cursor:
                    cursor.execute("CALL fix_bug_company_empty_record()")
            except Exception:
                return redirect("/base/?text={}".format("Wrong data format"))

            return redirect("/base/?text={}".format("Successful registration"))
    else:
        form = MyCompanyForm()
    return render(request, "company_registration.html", {"form": form})


def check_log(request):
    if request.POST:
        login = str(request.POST.get("uname"))
        password = str(request.POST.get("psw"))
        with connection.cursor() as cursor:
            cursor.callproc("check_login", [login, password])
            result = cursor.fetchone()[0]
            print(result)
        if result is None:
            return redirect("/base/?text={}".format("Login failed"))
    return redirect("/main_window/?login={}".format(login))


def main_window(request):
    login = str(request.GET.get("login"))
    rent_status = str(request.GET.get("rent_status"))
    if rent_status == "success":
        ca_id = str(request.GET.get("car_id"))
        query = f"SELECT id FROM carrental_client WHERE login = '{login}'"
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
        cl_id = data[0][0]
        rental = Rental.objects.create(
            client_id=Client.objects.get(id=cl_id),
            car_id=Car.objects.get(id=ca_id),
            station_id=None,
            start_date=timezone.now(),
            end_date=None,
            rental_status="rented",
        )
        rental.save()
        query = f"UPDATE carrental_car SET car_status = 'rented' where id = {ca_id}"
        with connection.cursor() as cursor:
            cursor.execute(query)
    query = "SELECT c.car_status, m.name, m.seats_number, m.doors_number, m.produced_date, c.id FROM carrental_car c JOIN carrental_carmodel m ON c.car_model_id = m.id"
    with connection.cursor() as cursor:
        with open("views/car_model_car.sql") as view:
            query = view.read()
            cursor.execute(query)
            data = cursor.fetchall()
    cars_list = [
        {
            "model": car[1],
            "seats_number": car[2],
            "doors_number": car[3],
            "status": car[0],
            "date_produced": car[4],
            "id": car[5],
        }
        for car in data
    ]
    p = Paginator(cars_list, 10)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    context = {"page_obj": page_obj, "login": login, "rent_status": rent_status}
    return render(request, "main_window.html", context)


def car_rent(request):
    car_id = str(request.GET.get("car_id"))
    login = str(request.GET.get("login"))
    if not car_id.isdigit():
        raise ValueError("Invalid id")
    car_info_query = f"SELECT m.doors_number, m.name, m.seats_number, m.trunk_capacity, m.produced_date, b.name, b.origin_country, t.driving_license, t.name, p.price_per_hour, p.price_per_kilometer FROM carrental_car c JOIN carrental_carmodel m ON c.car_model_id = m.id JOIN carrental_brand b ON b.id = m.brand_id_id JOIN carrental_cartype t ON t.id = m.type_id_id JOIN carrental_pricelist p ON p.id = m.price_list_id_id WHERE c.id = {car_id}"
    with connection.cursor() as cursor:
        cursor.execute(car_info_query)
        data = cursor.fetchall()[0]
    car_information = {
        "doors_number": data[0],
        "model_name": data[1],
        "seats_number": data[2],
        "trunk_capacity": data[3],
        "produced_date": data[4],
        "brand_name": data[5],
        "country_of_origin": data[6],
        "driving_license": data[7],
        "license_desc": data[8],
        "price_per_h": data[9],
        "price_per_km": data[10],
    }
    if request.method == "POST":
        query = "SELECT c.car_status, m.name, m.seats_number, m.doors_number, m.produced_date, c.id FROM carrental_car c JOIN carrental_carmodel m ON c.car_model_id = m.id"
    return render(
        request,
        "car_rent.html",
        {
            "login": login,
            "car_id": car_id,
            "car_info": car_information,
            "rental_status": "success",
        },
    )


def car_cancel(request):
    car_id = str(request.GET.get("car_id"))
    login = str(request.GET.get("login"))
    rental_id = str(request.GET.get("rental_id"))
    if not car_id.isdigit():
        raise ValueError("Invalid id")
    car_info_query = f"SELECT m.doors_number, m.name, m.seats_number, m.trunk_capacity, m.produced_date, b.name, b.origin_country, t.driving_license, t.name, p.price_per_hour, p.price_per_kilometer, c.id FROM carrental_car c JOIN carrental_carmodel m ON c.car_model_id = m.id JOIN carrental_brand b ON b.id = m.brand_id_id JOIN carrental_cartype t ON t.id = m.type_id_id JOIN carrental_pricelist p ON p.id = m.price_list_id_id WHERE c.id = {car_id}"
    with connection.cursor() as cursor:
        cursor.execute(car_info_query)
        data = cursor.fetchall()[0]

    with connection.cursor() as cursor:
        start_date_query = f"SELECT start_date FROM carrental_rental WHERE id={rental_id}"
        cursor.execute(start_date_query)
        start_date = cursor.fetchone()[0]

    car_information = {
        "doors_number": data[0],
        "model_name": data[1],
        "seats_number": data[2],
        "trunk_capacity": data[3],
        "produced_date": data[4],
        "brand_name": data[5],
        "country_of_origin": data[6],
        "driving_license": data[7],
        "license_desc": data[8],
        "price_per_h": data[9],
        "price_per_km": data[10],
    }

    return render(
        request,
        "car_cancel.html",
        {
            "login": login,
            "car_id": car_id,
            "car_info": car_information,
            "rent_start_date": start_date,
            "rental_id": rental_id,
            "cancel_status": "success"
        },
    )
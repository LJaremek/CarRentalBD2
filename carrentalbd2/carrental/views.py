from django.shortcuts import render, redirect
from .forms import MyForm, MyCompanyForm
from django.db import connection
from django.core.paginator import Paginator
from carrental.models import Client
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as log
from .models import Person, Company

# Create your views here.

def my_account(request):
    # try person
    username = request.POST.get("username")
    my_user_data = None
    query = ""
    user_data_dict = {}
    user_data = []
    my_user_data = []
    query = f"""\
    SELECT c.country, c.email, c.login, c.phone, p.first_name, p.pesel, p.surname, c.id \
    FROM carrental_client c JOIN carrental_person p ON c.id = p.parent_id \
    WHERE c.login = '{username}'"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        user_data = cursor.fetchall()
    if len(user_data) > 0:
        my_user_data = user_data[0]
        user_data_dict = {
            "first_name" : my_user_data[4],
            "pesel" : my_user_data[5],
            "surname" : my_user_data[6]
        }
    else:
        query = f"""\
        SELECT c.id, c.country, c.email, c.login, c.phone, k.name, k.nip, k.sector \
        FROM carrental_client c JOIN carrental_company k ON c.id = k.parent_id \
        WHERE c.login = '{username}'
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            user_data = cursor.fetchall()
        my_user_data = user_data[0]
        user_data_dict = {
            "name" : my_user_data[4],
            "nip" : my_user_data[5],
            "sector" : my_user_data[6]
        }
    user_data_dict["country"] = my_user_data[0]
    user_data_dict["email"] = my_user_data[1]
    user_data_dict["login"] = my_user_data[2]
    user_data_dict["phone"] = my_user_data[3]

    query = f"SELECT country, c.email, c.login, c.phone, k.name, k.nip, k.sector FROM client c JOIN company k ON c.id = k.id WHERE c.login = {username}"
    with connection.cursor() as cursor:
        cursor.execute(query)
        user_data = cursor.fetchall()

    return render(request, "my_account.html")


def log_screen_view(request):
    # loading procedures and fubctions to database
    with open('procedures/registration.sql', 'r') as sql_file:
        sql = sql_file.read()
    with connection.cursor() as cursor:
        cursor.execute(sql)
    with open('procedures/check_login.sql', 'r') as sql_file:
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
                    cursor.callproc('validate_input_data_person', [ username, email, password, repeated_password, phone, pesel, first_name, second_name ])
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
                        cursor.execute('CALL fix_bug_person_empty_record()')
            except:
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
                    cursor.callproc('validate_input_data_company', [
                        username,
                        email,
                        password,
                        repeated_password,
                        phone,
                        nip,
                        name,
                        sector
                        ]
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
                    cursor.execute('CALL fix_bug_company_empty_record()')
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
    with connection.cursor() as cursor:
        with open('views/car_model_car.sql') as view:
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
            "id": car[5]
        }
        for car in data
    ]
    p = Paginator(cars_list, 10)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    for el in page_obj:
        print(el)
    context = {"page_obj": page_obj, "username": login}
    return render(request, "main_window.html", context)

def car_rent(request):
    car_id = str(request.GET.get("car_id"))
    return render(request, "car_rent.html", {"text": id})
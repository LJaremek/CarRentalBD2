from django.shortcuts import render, redirect
from .forms import MyForm
from django.db import connection
from django.core.paginator import Paginator
from carrental.models import Client
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as log
from .models import Person, Company

# Create your views here.


def log_screen_view(request):
    with open('procedures/registration.sql', 'r') as sql_file:
        sql = sql_file.read()
    with connection.cursor() as cursor:
        cursor.execute(sql)
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
            with connection.cursor() as cursor:
                cursor.callproc('validate_input_data_person', [
                    username,
                    email,
                    password,
                    repeated_password,
                    phone,
                    pesel,
                    first_name,
                    second_name
                    ]
                )
                cursor.callproc('validate_pesel', [pesel])
                cursor.callproc('validate_phone_number', [phone])
                cursor.callproc('validate_email', [email])
            is_ok = True
            if password != repeated_password:
                is_ok = False
            if not phone.isnumeric():
                is_ok = False
            if not pesel.isnumeric():
                is_ok = False
            if is_ok:
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
                # temp fix to annoying db bug where there would be an empty client created
                query1 = "UPDATE carrental_person SET client_ptr_id=parent_id WHERE client_ptr_id != parent_id"
                query2 = "DELETE FROM carrental_client WHERE login=''"
                with connection.cursor() as cursor:
                    cursor.execute(query1)
                    cursor.execute(query2)

                # Create Django user
                print(username, email, password)
                user = User.objects.create_user(username, email, password)
                user.save()

                return redirect("/base/?text={}".format("Successful registration"))
            return render(request, "client_registration.html", {"form": form})
    else:
        form = MyForm()
    return render(request, "client_registration.html", {"form": form})


def registration_company(request):
    if request.method == "POST":
        form = MyForm(request.POST)
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
            is_ok = True
            if password != repeated_password:
                is_ok = False
            if not phone.isnumeric():
                is_ok = False
            if not nip.isnumeric():
                is_ok = False
            if is_ok:
                client = Client.objects.create(
                    login=username,
                    email=email,
                    password=password,
                    phone=phone,
                    country=country,
                )
                comapny = Company.objects.create(
                    nip=nip, name=name, sector=sector, parent=client
                )
                comapny.save()
                return redirect("/base/?text={}".format("Successful registration"))
            return render(request, "company_registration.html", {"form": form})
    else:
        form = MyForm()
    return render(request, "company_registration.html", {"form": form})


def check_log(request):
    if request.POST:
        login = request.POST.get("uname")
        password = request.POST.get("psw")
        try:
            user = authenticate(request, username=login, password=password)
            if user is not None:
                log(request, user)
            else:
                return render(request, "base.html", {"text": "login failed"})
            client = Client.objects.get(login=login)
        except Exception:
            return render(request, "base.html", {"text": "Wrong login"})
        if password != client.password:
            return render(request, "base.html", {"text": "Wrong password"})
        # if hash(password) == client.password
    query = "SELECT c.car_status, m.name, m.seats_number, m.doors_number, m.produced_date FROM carrental_car c JOIN carrental_carmodel m ON c.car_model_id = m.id"
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    cars_list = [
        {
            "model": car[1],
            "seats_number": car[2],
            "doors_number": car[3],
            "status": car[0],
            "date_produced": car[4],
        }
        for car in data
    ]
    p = Paginator(cars_list, 10)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    for el in page_obj:
        print(el)

    context = {"page_obj": page_obj}
    return render(request, "main_window.html", context)

from django.shortcuts import render, redirect
from .forms import MyForm
from carrental.models import Client
from django.http import HttpResponse
from .models import Person, Company

# Create your views here.


def log_screen_view(request):
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
                person = Person.objects.create(
                    pesel=pesel,
                    first_name=first_name,
                    second_name=second_name,
                    parent=client,
                )
                person.save()
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
                person = Company.objects.create(
                    nip=nip, name=name, sector=sector, parent=client
                )
                person.save()
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
            client = Client.objects.get(login=login)
        except Exception:
            return render(request, "base.html", {"text": "Wrong log data"})
        if password == client.password:
            # if hash(password) == client.password
            context = {"client": client}
            return render(request, "main_window.html", context)
        else:
            return render(request, "base.html", {"text": "Wrong log data"})

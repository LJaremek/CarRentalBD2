from django.shortcuts import render, redirect
from .forms import MyForm
from carrental.models import Client

# Create your views here.

def log_screen_view(request):
    return render(request, "base.html", {"data_error": False})


def registration(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            repeated_password = form.cleaned_data['repeated_password']
            phone = form.cleaned_data['phone']
            country = form.cleaned_data['country']
            pesel = form.cleaned_data['pesel']
            first_name = form.cleaned_data['first_name']
            second_name = form.cleaned_data['second_name']
            # Process the form data or save it to the database
            is_ok = True
            if password != repeated_password:
                is_ok = False
            if not phone.isnumeric():
                is_ok = False
            if not pesel.isnumeric():
                is_ok = False
            if is_ok:
                return redirect("/base/")
            return render(request, "client_registration.html", {'form': form})
    else:
        form = MyForm()
    return render(request, "client_registration.html", {'form': form})


def check_log(request):
    if request.POST:
        login = request.POST.get("uname")
        password = request.POST.get("psw")
        try:
            client = Client.objects.get(login=login)
        except Exception:
            return render(request, "base.html", {"data_error": True})
        if password == client.password:
        # if hash(password) == client.password
            context = {"client": client}
            return render(request, "main_window.html", context)
        else:
            return render(request, "base.html", {"data_error": True})

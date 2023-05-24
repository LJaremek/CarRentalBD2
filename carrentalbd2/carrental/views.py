from django.shortcuts import render
from carrental.models import Client

# Create your views here.

def log_screen_view(request):
    return render(request, "base.html", {"data_error": False})

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
from django.shortcuts import render

# Create your views here.

def log_screen_view(request):
    return render(request, "base.html", {})
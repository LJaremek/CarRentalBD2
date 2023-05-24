from django.shortcuts import render

# Create your views here.
def entry_page(request):
    return render(request, "entry_page.html", {})
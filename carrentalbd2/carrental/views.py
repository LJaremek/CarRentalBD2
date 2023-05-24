from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import connection  # may God have mercy on our souls
from django.contrib.auth.decorators import login_required
from .models import Car, CarModel, CarType


def about(request):
    # caveman moment
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
    return render(request, "about.html", {"page_obj": page_obj})


@login_required
def profile(request):
    return render(request, "profile.html", {})

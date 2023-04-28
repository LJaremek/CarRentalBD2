import matplotlib.pyplot as plt
from carrental.models import Brand, Repair, Car, CarModel
from django.db.models import Count


def car_brands():
    fig, ax = plt.subplots()
    origin_countires = Brand.objects.values("origin_country").annotate(
        num_brands=Count("id")
    )
    countires = []
    numbers = []
    for oc in origin_countires:
        countires.append(oc["origin_country"])
        numbers.append(oc["num_brands"])
    ax.bar(countires, numbers)
    ax.set_ylabel("amount")
    ax.set_title("Number of brands by country of origin")
    ax.legend(title="Origin country")
    return fig


def repair_realization():
    fig, ax = plt.subplots()
    repairs = Repair.objects.all()
    realizator = ["Insurance company", "Repair workshop"]
    numbers = [0, 0]
    for r in repairs:
        if r.insurance_company_id is None:
            numbers[1] += 1
        if r.repair_workshop_id is None:
            numbers[0] += 1
    ax.bar(realizator, numbers)
    ax.set_ylabel("amount")
    ax.set_title("Number of realized repairs by realizator")
    return fig


def car_by_brand():
    fig, ax = plt.subplots()
    brand_car_counts = Car.objects.values("car_model__brand_id__name").annotate(
        total_cars=Count("car_model__brand_id")
    )
    brand_names = []
    car_counts = []
    for brand_count in brand_car_counts:
        brand_names.append(brand_count["car_model__brand_id__name"])
        car_counts.append(brand_count["total_cars"])
    ax.bar(brand_names, car_counts)
    ax.set_ylabel("amount")
    ax.set_title("Amount of possessed cars of each brand")
    return fig

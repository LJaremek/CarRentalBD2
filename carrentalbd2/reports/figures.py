import matplotlib.pyplot as plt
from carrental.models import Brand, Repair, Car
from django.db.models import Count
from django.db import connection


def car_brands():
    fig, ax = plt.subplots(figsize=(10, 10))
    origin_countires = Brand.objects.values("origin_country").annotate(
        num_brands=Count("id")
    )
    countires = []
    numbers = []
    for oc in origin_countires:
        countires.append(oc["origin_country"])
        numbers.append(oc["num_brands"])
    ax.bar(countires, numbers)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='x', labelsize=10)
    ax.set_ylabel("amount")
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
    return fig


def car_by_brand():
    fig, ax = plt.subplots(figsize=(10, 10))
    brand_car_counts = Car.objects.values("car_model__brand_id__name").annotate(
        total_cars=Count("car_model__brand_id")
    )
    brand_names = []
    car_counts = []
    for brand_count in brand_car_counts:
        brand_names.append(brand_count["car_model__brand_id__name"])
        car_counts.append(brand_count["total_cars"])
    ax.bar(brand_names, car_counts)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='x', labelsize=12)
    ax.set_ylabel("amount")
    return fig


def demand_by_car_model():
    fig, ax = plt.subplots(figsize=(11, 11))
    with connection.cursor() as cursor:
        cursor.callproc('count_rental_by_car_model')
        result = cursor.fetchall()
    car_model_names = []
    rental_counts = []
    for row in result:
        car_model_names.append(row[0])
        rental_counts.append(row[1])
    ax.bar(car_model_names, rental_counts)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='x', labelsize=10)
    ax.set_ylabel("amount")
    return fig


def repair_costs_by_car_model():
    fig, ax = plt.subplots(figsize=(9, 9))
    with connection.cursor() as cursor:
        cursor.callproc('count_costs_by_car_model')
        result = cursor.fetchall()
    car_model_names = []
    repair_counts = []
    repair_sums = []
    for row in result:
        car_model_names.append(row[0])
        repair_counts.append(row[1])
        repair_sums.append(row[2] / 1000)
    bar_positions = range(len(car_model_names))
    print(car_model_names)
    print(repair_counts)
    print(repair_sums)
    width = 0.4
    ax.bar(bar_positions, repair_counts, width=width, label='Repair Counts')
    ax.bar([p + width for p in bar_positions], repair_sums, width=width, label='Repair Sums')
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='x', labelsize=10)
    ax.set_ylabel("amount")
    ax.set_xticks(bar_positions)  # Set the x-axis tick positions
    ax.set_xticklabels(car_model_names, rotation=45, ha='right', fontsize=10)
    return fig

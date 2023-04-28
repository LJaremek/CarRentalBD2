import matplotlib.pyplot as plt
from carrental.models import Brand
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

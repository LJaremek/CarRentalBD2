from django.db import models

CAR_STATUS = (
    ("free", "Free"),
    ("rented", "Rented"),
    ("service", "Service"),
    ("pending", "Pending"),
)


class CarInfo(models.Model):
    car_brand = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50)
    seats_number = models.IntegerField()
    doors_number = models.IntegerField()
    capacity = models.IntegerField()  # litres


class CarModel(models.Model):
    name = models.CharField(max_length=50)
    car_info = models.ForeignKey(CarInfo, null=True, on_delete=models.SET_NULL)


class Car(models.Model):
    car_status = models.CharField(
        choices=CAR_STATUS,
        default="free",
        max_length=15
    )

    car_model = models.ForeignKey(
        CarModel,
        null=True,
        on_delete=models.SET_NULL
        )

    produced_date = models.DateTimeField()


class User(models.Model):
    pass


class Rental(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    car = models.OneToOneField(Car, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

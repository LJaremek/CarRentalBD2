from django.db import models
from phone_field import PhoneField
from django.core.validators import MaxValueValidator
from djmoney.models.fields import MoneyField

CAR_STATUS = (
    ("free", "Free"),
    ("rented", "Rented"),
    ("service", "Service"),
    ("pending", "Pending"),
)

RENTAL_STATUS = (
    ("finished", "Finished"),
    ("ongoing", "Ongoing"),
    ("booked", "Booked"),
)

class User(models.Model):
    name = models.CharField(max_length=50, null=False)
    login = models.CharField(max_length=50, unique=True)
    #może zamiast tego emial?
    #email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50, null=False) #to do form, hash
    phone = PhoneField(blank=True, unique=True)
    citizenship = models.CharField(max_length=50, null=False)
    document_name = models.CharField(max_length=50)
    document_id = models.CharField(max_length=50)


class RentalBase(models.Model):
    location = models.CharField(max_length=100, unique=True, null=False)


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

class Rental(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    car = models.OneToOneField(Car, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rental_base = models.ForeignKey(RentalBase, null=False, on_delete=models.SET_NULL)
    rental_status = models.CharField(choices=RENTAL_STATUS, null=False)


class Report(models.Model):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=False)
    rental = models.OneToOneField(Rental, on_delete=models.SET_NULL, null=False)
    description = models.CharField(max_length=255, null=False)
    rate = models.PositiveIntegerField(
        validators=[MaxValueValidator(10)],
        null=False
        )

class Insurance(models.Model):
    car = models.ForeignKey(Car, null=False, on_delete=models.SET_NULL)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    company = models.CharField(max_length=150)


class Repair(models.Model):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=False)
    cost = MoneyField(max_digits=10, decimal_places=2, default_currency='PLN')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    car_repair_shop = models.CharField(max_length=50, null=False)


class CarFault(models.Model):
    report = models.ForeignKey(Report, null=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=False)
    repair = models.ForeignKey(Repair, null=True, on_delete=models.CASCADE)








from django.db import models
from django.core.validators import MaxValueValidator
from .xor_relationship import XORForeignKey

CAR_STATUS = (
    ("free", "Free"),
    ("rented", "Rented"),
    ("service", "Service"),
    ("pending", "Pending"),
)

RENTAL_STATUS = (("finished", "Finished"), ("ongoing", "Ongoing"), ("booked", "Booked"))


class Client(models.Model):
    login = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, null=False)  # to do form, hash
    phone = models.CharField(max_length=10, unique=True, null=True)
    country = models.CharField(max_length=50, null=True)


class Person(Client):
    pesel = models.CharField(max_length=20, null=False, unique=True)
    first_name = models.CharField(max_length=50, null=False, unique=False)
    second_name = models.CharField(max_length=50, null=False, unique=False)
    parent = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="children_person",
        default=None
        )


class Company(Client):
    nip = models.CharField(max_length=50, null=False, unique=True)
    sector = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null=False, unique=True)
    parent = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="children_company",
        default=None
        )


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    origin_country = models.CharField(max_length=50, null=True)


class CarType(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False)
    driving_license = models.CharField(max_length=10, null=False)


class PriceList(models.Model):
    price_per_hour = models.PositiveIntegerField(null=False)
    price_per_kilometer = models.PositiveIntegerField(null=False)


class CarModel(models.Model):
    brand_id = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
    type_id = models.ForeignKey(CarType, null=True, on_delete=models.SET_NULL)
    price_list_id = models.ForeignKey(PriceList, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, null=False, unique=False)
    seats_number = models.PositiveIntegerField(null=False)
    trunk_capacity = models.PositiveIntegerField(null=True)
    doors_number = models.PositiveIntegerField(null=False)
    produced_date = models.DateField(blank=True, null=True)


class RentalStation(models.Model):
    address = models.CharField(max_length=100, null=False)


class Car(models.Model):
    car_status = models.CharField(choices=CAR_STATUS, default="free", max_length=15)
    rental_station_id = models.ForeignKey(
        RentalStation, null=True, on_delete=models.CASCADE
    )
    car_model = models.ForeignKey(CarModel, null=True, on_delete=models.CASCADE)
    plate = models.CharField(null=False, unique=True, max_length=20)
    insurance_start_date = models.DateTimeField(null=True)
    insurance_end_date = models.DateTimeField(null=True)

class Rental(models.Model):
    client_id = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    car_id = models.ForeignKey(Car, null=True, on_delete=models.SET_NULL)
    station_id = models.ForeignKey(RentalStation, null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS, null=False)


class Refund(models.Model):
    rental_id = models.OneToOneField(Rental, null=True, on_delete=models.SET_NULL)
    amount = models.PositiveBigIntegerField(null=True)
    description = models.TextField(max_length=250, null=True)
    apologise_message = models.TextField(max_length=250, null=True)


class TrafficViolation(models.Model):
    rental_id = models.OneToOneField(Rental, null=True, on_delete=models.SET_NULL)
    fine = models.PositiveIntegerField(null=True)
    description = models.TextField(max_length=250, null=False)
    penalty_points = models.PositiveIntegerField(null=True)


class Report(models.Model):
    rental_id = models.OneToOneField(Rental, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=250, null=False)
    rate = models.PositiveIntegerField(validators=[MaxValueValidator(10)], null=False)


class RepairWorkshop(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    telephone = models.CharField(max_length=10, null=True, unique=True)
    address = models.CharField(max_length=50, null=False)


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    telephone = models.CharField(max_length=10, null=True, unique=True)
    ac = models.BooleanField(null=False)


class Repair(models.Model):
    repair_workshop_id = XORForeignKey(
        RepairWorkshop, on_delete=models.CASCADE, xor_fields=["insurance_company_id"], null=True
    )
    insurance_company_id = XORForeignKey(
        InsuranceCompany, on_delete=models.CASCADE, xor_fields=["repair_workshop_id"], null=True
    )
    cost = models.PositiveIntegerField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)


class CarFault(models.Model):
    report_id = models.ForeignKey(Report, null=False, on_delete=models.CASCADE)
    repair_id = models.ForeignKey(Repair, null=True, on_delete=models.CASCADE)
    description = models.TextField(max_length=250, null=False)


class Insurance(models.Model):
    car = models.ForeignKey(Car, null=True, on_delete=models.SET_NULL)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    company = models.CharField(max_length=150)


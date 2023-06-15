from django.core import management
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command


@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == "carrental":
        model_files = [
            "CarType.json",
            "Brand.json",
            "PriceList.json",
            "CarModel.json",
            "Client.json",
            "Person.json",
            "Company.json",
            "RentalStation.json",
            "Car.json",
            "InsuranceCompany.json",
            "RepairWorkshop.json",
            "Repair.json",
            "Rental.json",
            "TrafficViolation.json",
            "Raport.json",
            "Refund.json",
            "CarFault.json",
        ]
        for file in model_files:
            call_command("loaddata", file)

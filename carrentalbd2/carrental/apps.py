from django.apps import AppConfig
from django.core.management import call_command

class CarrentalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carrental'

    def ready(self):
        model_files = [
            'CarType.json',
            'Brand.json',
            'PriceList.json',
            'CarModel.json',

        ]
        for file in model_files:
            call_command('loaddata', file)

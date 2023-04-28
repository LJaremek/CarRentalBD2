from django.contrib import admin
from .models import BrandOrigin, RepairRealization, CarByBrand

admin.site.register(BrandOrigin)
admin.site.register(RepairRealization)
admin.site.register(CarByBrand)

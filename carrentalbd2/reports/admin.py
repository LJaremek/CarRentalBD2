from django.contrib import admin
from .models import *


admin.site.register(BrandOrigin, BrandOriginAdmin)
admin.site.register(RepairRealization, RepairRealizationAdmin)
admin.site.register(CarByBrand, CarByBrandAdmin)

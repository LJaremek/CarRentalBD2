import io
import urllib.parse
import base64
from django.db import models
from django_matplotlib import MatplotlibFigureField
from django.contrib import admin
from .figures import car_brands, repair_realization, car_by_brand


def convert_chart(plot):
    buffer = io.BytesIO()
    plot.savefig(buffer, format="png")
    buffer.seek(0)
    image = buffer.getvalue()
    buffer.close()
    chart_url = urllib.parse.quote(base64.b64encode(image))
    return chart_url


class BrandOriginAdmin(admin.ModelAdmin):
    change_list_template = "chart.html"

    def changelist_view(self, request, extra_context=None):
        self.queryset = self.model.objects.filter()
        chart = car_brands()
        extra_context = {}
        extra_context["chart_url"] = convert_chart(chart)
        extra_context["title"] = "Number of brands by country of origin"

        return super().changelist_view(request, extra_context=extra_context)


class BrandOrigin(models.Model):
    figure = MatplotlibFigureField(figure="car_brands")


class RepairRealizationAdmin(admin.ModelAdmin):
    change_list_template = "chart.html"

    def changelist_view(self, request, extra_context=None):
        self.queryset = self.model.objects.filter()
        chart = repair_realization()
        extra_context = {}
        extra_context["chart_url"] = convert_chart(chart)
        extra_context["title"] = "Number of realized repairs by realizator"
        return super().changelist_view(request, extra_context=extra_context)


class RepairRealization(models.Model):
    figure = MatplotlibFigureField(figure="repair_realization")


class CarByBrandAdmin(admin.ModelAdmin):
    change_list_template = "chart.html"

    def changelist_view(self, request, extra_context=None):
        self.queryset = self.model.objects.filter()
        chart = car_by_brand()
        extra_context = {}
        extra_context["chart_url"] = convert_chart(chart)
        extra_context["title"] = "Amount of possessed cars of each brand"
        return super().changelist_view(request, extra_context=extra_context)


class CarByBrand(models.Model):
    figure = MatplotlibFigureField(figure="car_by_brand")

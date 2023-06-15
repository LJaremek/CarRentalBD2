import io
import urllib.parse
import base64
from typing import Callable
from django.db import models
from django_matplotlib import MatplotlibFigureField
from django.contrib import admin
from .figures import *


def create_content(plotter: Callable, title: str):
    chart = plotter()
    extra_context = {}
    extra_context["chart_url"] = convert_chart(chart)
    extra_context["title"] = title
    return extra_context


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
        extra_context = create_content(
            car_brands, "Number of brands by country of origin"
        )
        return super().changelist_view(request, extra_context=extra_context)


class BrandOrigin(models.Model):
    figure = MatplotlibFigureField(figure="car_brands")


class RepairRealizationAdmin(admin.ModelAdmin):
    change_list_template = "chart.html"

    def changelist_view(self, request, extra_context=None):
        self.queryset = self.model.objects.filter()
        extra_context = create_content(
            repair_realization, "Number of realized repairs by realizator"
        )
        return super().changelist_view(request, extra_context=extra_context)


class RepairRealization(models.Model):
    figure = MatplotlibFigureField(figure="repair_realization")


class CarByBrandAdmin(admin.ModelAdmin):
    change_list_template = "chart.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = create_content(
            car_by_brand, "Amount of possessed cars of each brand"
        )
        return super().changelist_view(request, extra_context=extra_context)


class CarByBrand(models.Model):
    figure = MatplotlibFigureField(figure="car_by_brand")


class DemandByCarModelAdmin(admin.ModelAdmin):
    change_list_template = "chart.html"

    def changelist_view(self, request, extra_context=None):
        self.queryset = self.model.objects.filter()
        extra_context = create_content(
            demand_by_car_model, "Amount of rent by car model"
        )
        return super().changelist_view(request, extra_context=extra_context)


class DemandByCarModel(models.Model):
    figure = MatplotlibFigureField(figure="demand_by_car_model")


class RepairCostsByCarModelAdmin(admin.ModelAdmin):
    change_list_template = "chart.html"

    def changelist_view(self, request, extra_context=None):
        self.queryset = self.model.objects.filter()
        extra_context = create_content(
            repair_costs_by_car_model,
            "Amount of repair and total cost of them /1000 by car model",
        )
        return super().changelist_view(request, extra_context=extra_context)


class RepairCostsByCarModel(models.Model):
    figure = MatplotlibFigureField(figure="repair_costs_by_car_model")

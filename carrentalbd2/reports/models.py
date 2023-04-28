from django.db import models
from django_matplotlib import MatplotlibFigureField


class CarBrand(models.Model):
    figure = MatplotlibFigureField(figure="car_brands")

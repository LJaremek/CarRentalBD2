from .models import Car


def get_all_cars(skip = 0, limit = 10):
    """
    Retrieves cars from database with pagination
    """
    return Car.objects.all()[skip:limit]

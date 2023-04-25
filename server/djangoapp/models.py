from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `
class CarMake(models.Model):
    # - Name
    name = models.CharField(null=False, max_length=30)
    # - Description
    description = models.CharField(max_length=1000)
    # - Any other fields you would like to include in car make model
    # - __str__ method to print a car make object
    def __str__(self):
            return "Name: " + self.name + "," + \
                "Description: " + self.description


class CarModel(models.Model):
    # - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    # - Name
    name = models.CharField(max_length=30)
    # - Dealer id, used to refer a dealer created in cloudant database
    dealerid = models.IntegerField()
    # - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    types = [(SEDAN, 'Sedan'), (SUV, 'SUV'),(WAGON, 'Wagon')]
    cartype = models.CharField(max_length=5, choices=types)
    # - Year (DateField)
    year = models.DateField()
    # - Any other fields you would like to include in car model
    # - __str__ method to print a car make object
    def __str__(self):
            return "Name: " + self.name + "," + \
                "Car make: " + self.cartype


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data

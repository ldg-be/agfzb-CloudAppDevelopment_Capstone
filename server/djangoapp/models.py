from django.db import models
from django.utils.timezone import now


# Create your models here.
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


class DealerReview:
    def __init__(self, car_make, car_model, car_year, dealership, id, name, purchase, purchase_date, review, sentiment):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment
        
    def __str__(self):
        return "Reviewers name: " + self.name

class CarDealer: 
    def __init__(self, address,city, full_name, id, lat, long, short_name, st, zip, state):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
        self.state = state

    def __str__(self):
        return "Dealer name: " + self.full_name

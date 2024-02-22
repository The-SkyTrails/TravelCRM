from django.db import models

BASE_CURRENCY = [("Yes", "Yes"), ("No", "No")]


class Country(models.Model):
    country_name = models.CharField(max_length=100)
    sort_name = models.CharField(max_length=4)
    nationality = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    image = models.FileField(upload_to="vehicle/")
    sightseeing_capacity = models.IntegerField()
    transfer_capacity = models.IntegerField()
    date = models.DateField(auto_now_add=True)


class Driver(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    mobile = models.CharField(max_length=15)
    alternate_no = models.CharField(max_length=15, blank=True, null=True)
    passport = models.CharField(max_length=20)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    car_image = models.FileField(upload_to="driver/car/")
    licence_image = models.FileField(upload_to="driver/license/")
    address = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Meal_Plan(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Hotel_Category(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Ferry_Class(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Expense_servive_type(models.Model):
    name = models.CharField(max_length=100)
    remarks = models.TextField()
    date = models.DateField(auto_now_add=True)


class Extra_Meal_Price(models.Model):
    name = models.CharField(max_length=100)
    adult = models.FloatField()
    child = models.FloatField()
    infant = models.FloatField()
    date = models.DateField(auto_now_add=True)


class Flight(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to="flight/")
    date = models.DateField(auto_now_add=True)


class Currency(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    base_currency = models.CharField(max_length=20, choices=BASE_CURRENCY)
    date = models.DateField(auto_now_add=True)


class Lead_source(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)


class Bank(models.Model):
    bank_name = models.CharField(max_length=100)
    account_details = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zip = models.IntegerField()
    address = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Restaurent_location(models.Model):
    name = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Restaurent_type(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Special_days(models.Model):
    name = models.CharField(max_length=100)
    block_out_from_date = models.DateField()
    block_out_to_date = models.DateField()
    date = models.DateField(auto_now_add=True)


class Room_type(models.Model):
    name = models.CharField(max_length=100)
    remarks = models.TextField()
    date = models.DateField(auto_now_add=True)


class Hotel_location(models.Model):
    name = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Amenities(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Arrival_Departure(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Visa(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    adult_cost = models.FloatField()
    child_cost = models.FloatField()
    infant_cost = models.FloatField()
    date = models.DateField(auto_now_add=True)


class Transfer_location(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Guide(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    mobile = models.CharField(max_length=15)
    alternate_no = models.CharField(max_length=15)
    id_passport = models.CharField(max_length=50)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    car_image = models.FileField(upload_to="Guide/Car/")
    license_image = models.FileField(upload_to="Guide/Licence/")
    destination_covered = models.ManyToManyField(Destination)
    language = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)


class ExtraMeal(models.Model):
    name = models.CharField(max_length=100)
    meal_duration = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    location = models.ForeignKey(Restaurent_location, on_delete=models.CASCADE)
    # restaurant = models.ForeignKey()
    short_description = models.TextField()
    description = models.TextField()
    inclusions = models.TextField()
    useful_information = models.TextField()
    import_notes = models.TextField()

from django.db import models
import os
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import datetime
from django.core.cache import cache

BASE_CURRENCY = [
    ("Yes","Yes"),
    ("No","No")
]

INTER_DOMES_CHOICES = [
    ("International","International"),
    ("Domestic","Domestic")
]

MEAL_PREFRENCE = [
    ("Veg/Non Veg","Veg/Non Veg"),
    ("Pure Veg/Jain Meals","Pure Veg/Jain Meals")
]

ARRIVAL_DEPARTURE = [
    ("NA","NA"),
    ("Arrival","Arrival"),
    ("Departure","Departure")
]

SERVICE_TYPE = [
    ("Hotel","Hotel"),
    ("Meals","Meals"),
    ("Sightseeing","Sightseeing"),
    ("Transfer","Transfer"),
    ("Visa Service","Visa Service"),
    ("Flight","Flight"),
    ("Activity","Activity"),
    ("Ferry","Ferry"),
    ("Boat","Boat"),
    ("Insurance","Insurance"),
]

TRANSFER_TYPE = [
    ("SIC","SIC"),
    ("PVT","PVT"),
    ("SIC/PVT","SIC/PVT"),
]

DAYS_CHOICES = [
    ("All","All"),
    ("Sunday","Sunday"),
    ("Monday","Monday"),
    ("Tuesday","Tuesday"),
    ("Wednesday","Wednesday"),
    ("Thursday","Thursday"),
    ("Friday","Friday"),
    ("Saturday","Saturday")   
]

COMPANY_CHOICES = [
    ("The Skytrails","The Skytrails")
]

USER_TYPE_CHOICES = [
    ("Admin","Admin"),
    ("Operation Person","Operation Person"),
    ("Sales Person","Sales Person"),
    ("Hotel Reservation Person","Hotel Reservation Person"),
    ("Visa Service","Visa Service"),
    ("Account","Account"),
    ("Ground Operation","Ground Operation"),
    ("Hr","Hr"), 
    ("Customer Service","Customer Service"), 
    ("Marketing Person","Marketing Person"), 
    ("Sales + Marketing Person","Sales + Marketing Person"), 
]

LEAD_STATUS_CHOICES = [
    ("New Lead","New Lead"),
    ("Connected","Connected"),
    ("Quotation Send","Quotation Send"),
    ("Payment Processing","Payment Processing"),
    ("Payment Done","Payment Done"),
    ("Lost","Lost"),
    ("Completed","Completed")
]


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100)
    sort_name = models.CharField(max_length=4)
    nationality = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class State(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    
class Vehicle(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    image = models.FileField(upload_to="vehicle/")
    sightseeing_capacity = models.IntegerField()
    transfer_capacity = models.IntegerField()
    date = models.DateField(auto_now_add=True)


class Driver(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    mobile = models.CharField(max_length=15)
    alternate_no = models.CharField(max_length=15,blank=True, null=True)
    passport = models.CharField(max_length=20)
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    car_image = models.FileField(upload_to="driver/car/")
    licence_image = models.FileField(upload_to="driver/license/")
    address = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    
    
class Meal_Plan(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    

class Hotel_Category(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)   
    
    
class Ferry_Class(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    
    
class Expense_servive_type(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    remarks = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    
class Extra_Meal_Price(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    adult = models.FloatField()
    child = models.FloatField()
    infant = models.FloatField()
    date = models.DateField(auto_now_add=True)
    
    
class Flight(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to="flight/")
    date = models.DateField(auto_now_add=True)
    
    
class Currency(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    base_currency = models.CharField(max_length=20,choices=BASE_CURRENCY)
    date = models.DateField(auto_now_add=True)
    
class Lead_source(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)


class Bank(models.Model):
    id=models.AutoField(primary_key=True)
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
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Restaurent_location(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Restaurent_type(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Special_days(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    block_out_from_date = models.DateField()
    block_out_to_date = models.DateField()
    date = models.DateField(auto_now_add=True)


class Room_type(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    remarks = models.TextField()
    date = models.DateField(auto_now_add=True)


class Hotel_location(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Amenities(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Arrival_Departure(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Visa(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    adult_cost = models.FloatField()
    child_cost = models.FloatField()
    infant_cost = models.FloatField()
    date = models.DateField(auto_now_add=True)


class Transfer_location(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


class Guide(models.Model):
    id=models.AutoField(primary_key=True)
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
    
    
class Restaurent(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to="Restaurent/")
    timing = models.CharField(max_length=20)
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE)
    restaurant_location = models.ForeignKey(Restaurent_location, on_delete=models.CASCADE)
    meal_prefrence = models.CharField(max_length=30,choices=MEAL_PREFRENCE)
    landmark = models.CharField(max_length=100)
    restaurent_type = models.ManyToManyField(Restaurent_type)
    type = models.ForeignKey(Extra_Meal_Price,on_delete=models.CASCADE)
    address = models.TextField()
    contact_person = models.CharField(max_length=100)
    contact_person_phone = models.CharField(max_length=20)
    contact_person_email = models.EmailField()
    landline_no = models.CharField(max_length=30)
    restaurent_details = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    
class Hotel(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE)
    category = models.ForeignKey(Hotel_Category,on_delete=models.CASCADE)
    hotel_image = models.FileField(upload_to="Hotel/hotel_image/")
    contact_person = models.CharField(max_length=100)
    tel_no = models.CharField(max_length=20)
    mob_no = models.CharField(max_length=20)
    reservation_email = models.EmailField()
    amenities = models.ManyToManyField(Amenities)
    hotel_contract = models.FileField(upload_to="Hotel/hotel_contract/")
    room_type = models.ManyToManyField(Room_type)
    meal_plan = models.ManyToManyField(Meal_Plan)
    hotel_address = models.CharField(max_length=100)
    details = models.TextField()
    supplier_own = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    

class ExtraMeal(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    meal_duration = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurent, on_delete=models.CASCADE)
    short_description = models.TextField()
    description = models.TextField()
    inclusions = models.TextField()
    useful_information = models.TextField()
    import_notes = models.TextField()
    date = models.DateField(auto_now_add=True)
    
class Day(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Sightseeing(models.Model):
    id=models.AutoField(primary_key=True)
    activity_name = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE)
    activity_image = models.FileField(upload_to="Sightseeing/activity_image/")
    tour_duration = models.CharField(max_length=100)
    timings = models.CharField(max_length=100)
    operating_days = models.ManyToManyField(Day)
    details = models.TextField()
    date = models.DateField(auto_now_add=True)
    

class Service_type(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    
class Supplier(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_person_name = models.CharField(max_length=100)
    contact_person_designation = models.CharField(max_length=100)
    contact_person_email = models.EmailField()
    landline_no = models.CharField(max_length=20)
    mob_no = models.CharField(max_length=20)
    service_type = models.ManyToManyField(Service_type)
    contract = models.FileField(upload_to="Supplier/contract/")
    gst_vat = models.CharField(max_length=100)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    zip = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    
    
class Transfer(models.Model):
    id=models.AutoField(primary_key=True)
    transfer_name = models.CharField(max_length=100)
    transfer_type= models.CharField(max_length=20,choices=TRANSFER_TYPE)
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE)
    transfer_images = models.FileField(upload_to="Transfer/images/")
    tour_duration = models.CharField(max_length=100)
    timings = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    
class Itinerary(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE,related_name="destination")
    previous_destination = models.ForeignKey(Destination,on_delete=models.CASCADE,related_name="previous_destination")
    image = models.FileField(upload_to="Itinerary/images/")
    arrival_departure = models.CharField(max_length=10,choices=ARRIVAL_DEPARTURE)
    transfer = models.ManyToManyField(Transfer)
    sightseeing = models.ManyToManyField(Sightseeing)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    
class Folder(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

class Document(models.Model):
    id=models.AutoField(primary_key=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    date = models.DateField(auto_now_add=True)
    
    
class Role_Permission(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    

    
class CustomUser(AbstractUser):
    code = models.CharField(max_length=5)
    contact = models.CharField(max_length=15)
    user_type = models.CharField(max_length=50,choices=USER_TYPE_CHOICES,default="Admin")
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE)
    is_logged_in = models.BooleanField(default=False)
    tata_tele_agent_no = models.CharField(max_length=255,null=True,blank=True)
    
    
class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    users = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    assigned_company = models.CharField(max_length=50,choices=COMPANY_CHOICES)
    role = models.ForeignKey(Role_Permission,on_delete=models.CASCADE)
    reporting_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="reporting_to")
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    pin = models.CharField(max_length=10)
    address  = models.CharField(max_length=100)
    email_signature = models.TextField()
    registered_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="register_by")
       
    
class Lead(models.Model):
    id=models.AutoField(primary_key=True)
    enquiry_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15)
    inter_domes = models.CharField(max_length=20,choices=INTER_DOMES_CHOICES)
    destinations = models.ForeignKey(Destination,on_delete=models.CASCADE)
    from_date = models.DateField(auto_now_add=False)
    to_date = models.DateField(auto_now_add=False)   
    purpose_of_travel = models.CharField(max_length=100,blank=True, null=True)
    service_type = models.ForeignKey(Service_type,on_delete=models.CASCADE)
    query_title = models.CharField(max_length=100)
    budget = models.CharField(max_length=50,blank=True, null=True)
    adult = models.IntegerField()
    child = models.IntegerField(blank=True, null=True)
    infants = models.IntegerField(blank=True, null=True)
    lead_source = models.ForeignKey(Lead_source,on_delete=models.CASCADE)
    operation_person = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name="operation_person")
    sales_person = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="sales_person")
    other_information = models.TextField(blank=True, null=True)
    lead_status = models.CharField(max_length=50,choices=LEAD_STATUS_CHOICES)
    date = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    last_updated_at = models.DateTimeField(auto_now=True)
    
    
    def generate_case_id(self):
        current_date = datetime.date.today()
        current_month_abbrev = current_date.strftime("%b").upper()
        current_day = current_date.strftime("%d")
        serial_number = self.get_next_serial_number()
        self.case_id = f"{current_month_abbrev}{current_day}-{serial_number}"
        
        
    def get_next_serial_number(self):
        last_enquiry = Lead.objects.order_by("-id").first()
        if last_enquiry and last_enquiry.case_id:
            last_serial_number = int(last_enquiry.case_id.split("-")[1])
            next_serial_number = last_serial_number + 1
        else:
            next_serial_number = 1
        return f"{next_serial_number:05d}"
    
        
    def save(self, *args, **kwargs):
        if not self.enquiry_number:
            highest_enquiry = Lead.objects.order_by("-enquiry_number").first()
            if highest_enquiry:
                last_enquiry_number = int(highest_enquiry.enquiry_number)
                self.enquiry_number = str(last_enquiry_number + 1)
            else:
                self.enquiry_number = "100"

        super(Lead, self).save(*args, **kwargs)
        
class Attachment(models.Model):
    id=models.AutoField(primary_key=True)
    file = models.FileField(upload_to="Query/Quatation/",null=True,blank=True)
        
        
class Quatation(models.Model):
    id=models.AutoField(primary_key=True)
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='quotations')
    attachment = models.ManyToManyField(Attachment)
    date = models.DateField(auto_now_add=True)
    
    
class Notes(models.Model):
    id=models.AutoField(primary_key=True)
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='notes')
    notes = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    
class Payment(models.Model):
    leads = models.ForeignKey(Lead,on_delete=models.CASCADE)
    link_id = models.CharField(max_length=255)
    payment_link = models.URLField(max_length=200,)
    link_expiry_time = models.DateTimeField()
    
    
class Followup(models.Model):
    id=models.AutoField(primary_key=True)
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='followup')
    datetime = models.DateTimeField(auto_now_add=False)
    note = models.TextField(max_length=100)
    date = models.DateField(auto_now_add=True)

    
@receiver(post_save, sender=CustomUser)
def create_admin_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "Admin":
            Admin.objects.create(users=instance)
        

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "Admin":
        instance.admin.save()


    
    
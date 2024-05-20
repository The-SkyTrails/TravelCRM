from django.db import models
import os
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import datetime
from django.core.cache import cache
from django.utils import timezone

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
    ("Others","Others"),
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
    ("Pending","Pending"),
    ("Connected","Connected"),
    ("Quotation Send","Quotation Send"),
    ("Payment Processing","Payment Processing"),
    ("Payment Done","Payment Done"),
    ("Booking Confirmed","Booking Confirmed"),
    ("Lost","Lost"),
    ("Completed","Completed")
]


FOLLOWUP_TYPE = [
    ('followup', 'Follow Up'),
    ('task', 'Task'),
]

COLOUR_CHOICES = [
    ('Red', 'Red'),
    ('Green', 'Green'),
    ('Blue', 'Blue')
]

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100)
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
    adult = models.FloatField(default=0.0)
    child = models.FloatField(default=0.0)
    infant = models.FloatField(default=0.0)
    date = models.DateField(auto_now_add=True)
    
    
class Flight(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to="flight/")
    date = models.DateField(auto_now_add=True)
    
    
class Currency(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0.0)
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
    adult_cost = models.FloatField(default=0.0)
    child_cost = models.FloatField(default=0.0)
    infant_cost = models.FloatField(default=0.0)
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
    remarks = models.TextField()
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
    Login_CHOICES = [
    ("Yes","Yes"),
    ("No","No")
]
    code = models.CharField(max_length=5,null=True,blank=True)
    contact = models.CharField(max_length=15,null=True,blank=True)
    user_type = models.CharField(max_length=50,choices=USER_TYPE_CHOICES,default="Admin")
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE,null=True,blank=True)
    is_logged_in = models.CharField(max_length=50,choices=Login_CHOICES,default="No")
    tata_tele_agent_no = models.CharField(max_length=255,null=True,blank=True)
    ai_sensy_username = models.CharField(max_length=50,null=True,blank=True)
    authorization = models.CharField(max_length=255,null=True,blank=True)
    zoho_password = models.CharField(max_length=30,blank=True, null=True)
    
    
    
class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    users = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # role = models.ForeignKey(Role_Permission,on_delete=models.CASCADE)
    reporting_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="reporting_to",null=True,blank=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True,blank=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE,null=True,blank=True)
    pin = models.CharField(max_length=10,null=True,blank=True)
    address  = models.CharField(max_length=100,null=True,blank=True)
    # email_signature = models.TextField()
    registered_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="register_by",null=True,blank=True)
       
    
class Lead(models.Model):
    id=models.AutoField(primary_key=True)
    enquiry_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    alternate_mobile_number = models.CharField(max_length=15,blank=True, null=True)
    inter_domes = models.CharField(max_length=20,choices=INTER_DOMES_CHOICES,blank=True, null=True)
    destinations = models.ForeignKey(Destination,on_delete=models.CASCADE)
    from_date = models.DateField(auto_now_add=False)
    to_date = models.DateField(auto_now_add=False)   
    purpose_of_travel = models.CharField(max_length=100,blank=True, null=True)
    service_type = models.ForeignKey(Service_type,on_delete=models.CASCADE,blank=True, null=True)
    query_title = models.CharField(max_length=100)
    budget = models.CharField(max_length=50,blank=True, null=True)
    adult = models.IntegerField()
    child = models.CharField(max_length=50,blank=True, null=True)
    infants = models.CharField(max_length=50,blank=True, null=True)
    lead_source = models.ForeignKey(Lead_source,on_delete=models.CASCADE,blank=True, null=True)
    operation_person = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name="operation_person",blank=True, null=True)
    sales_person = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="sales_person")
    assigning_date = models.DateTimeField(auto_now=True)
    other_information = models.TextField(blank=True, null=True)
    lead_status = models.CharField(max_length=50,choices=LEAD_STATUS_CHOICES,blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    complete_package_cost = models.FloatField(default=0.0)
    received_package_cost = models.FloatField(default=0.0)
    balance_package_cost = models.FloatField(default=0.0)
    colour_code = models.CharField(max_length=20,choices=COLOUR_CHOICES)
    added_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True, null=True)
    net_cost = models.FloatField(default=0.0)
    markup = models.FloatField(default=0.0)
    tcs = models.FloatField(default=0.0)
    gst = models.FloatField(default=0.0)
    pg_card = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    booking_card_notes = models.TextField()
    last_updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True, null=True,related_name="last_update")
    
    
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
    
    
    
class ActivityHistory(models.Model):
    activity_type_choices = (
        ('Note', 'Note Added'),
        ('Followup', 'Followup Added'),
        ('Quotation', 'Quotation Added'),
        ('Payment', 'Payment Added'),
        ('Attachment', 'Attachment Added')
    )
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=activity_type_choices)
    datetime = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.activity_type} for {self.lead.name} at {self.datetime}"

class Attachment(models.Model):
    id=models.AutoField(primary_key=True)
    file = models.FileField(upload_to="Query/Quatation/",null=True,blank=True)
        
        
class Quatation(models.Model):
    id=models.AutoField(primary_key=True)
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='quotations')
    activity = models.OneToOneField(ActivityHistory, on_delete=models.CASCADE, related_name='quotation',null=True,blank=True)
    attachment = models.ManyToManyField(Attachment)
    date = models.DateField(auto_now_add=True)

class Notes(models.Model):
    id=models.AutoField(primary_key=True)
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='notes')
    activity = models.OneToOneField(ActivityHistory, on_delete=models.CASCADE, related_name='note',null=True,blank=True)
    notes = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    
class Followup(models.Model):
    id=models.AutoField(primary_key=True)
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='followup')
    type = models.CharField(max_length=20,choices=FOLLOWUP_TYPE)
    activity = models.OneToOneField(ActivityHistory, on_delete=models.CASCADE, related_name='followups',null=True,blank=True)
    datetime = models.DateTimeField(auto_now_add=False)
    note = models.TextField(max_length=100)
    archieve = models.BooleanField(default="True")
    date = models.DateField(auto_now_add=True)
   
class File(models.Model):
    id=models.AutoField(primary_key=True)
    file = models.FileField(upload_to="Query/Attachment/",null=True,blank=True)   
 
class ConfirmAttachment(models.Model):
    id=models.AutoField(primary_key=True)
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='attachment')
    activity = models.OneToOneField(ActivityHistory, on_delete=models.CASCADE, related_name='attachments',null=True,blank=True)
    attachment = models.ManyToManyField(File)
    date = models.DateField(auto_now_add=True)

class Messages(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Payment(models.Model):
    leads = models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='payments')
    activity = models.OneToOneField(ActivityHistory, on_delete=models.CASCADE, related_name='payment',null=True,blank=True)
    link_id = models.CharField(max_length=255)
    payment_link = models.URLField(max_length=200,)
    link_expiry_time = models.DateTimeField()
    
    
class BookingCard(models.Model):
    leads = models.ForeignKey(Lead,on_delete=models.CASCADE)
    product = models.CharField(max_length=30,choices=SERVICE_TYPE)
    name = models.CharField(max_length=100)
    supplier = models.CharField(max_length=100)
    netcost = models.FloatField(default=0.0)
    source = models.CharField(max_length=100)
    source_details = models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=50)
    vendor_payment = models.CharField(max_length=100)
    holding_date = models.DateField(auto_now=False,null=True,blank=True)
    updated_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    
    
@receiver(post_save, sender=CustomUser)
def create_admin_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "Admin":
            Admin.objects.create(users=instance)
        
        if instance.user_type == "Operation Person":
            Admin.objects.create(users=instance)
        
        if instance.user_type == "Sales Person":
            Admin.objects.create(users=instance)
        
        if instance.user_type == "Hotel Reservation Person":
            Admin.objects.create(users=instance)
        
        if instance.user_type == "Visa Service":
            Admin.objects.create(users=instance)
        
        
        if instance.user_type == "Account":
            Admin.objects.create(users=instance)
        
        
        if instance.user_type == "Ground Operation":
            Admin.objects.create(users=instance)
        
        if instance.user_type == "Hr":
            Admin.objects.create(users=instance)
        if instance.user_type == "Customer Service":
            Admin.objects.create(users=instance)
        if instance.user_type == "Marketing Person":
            Admin.objects.create(users=instance)
        
        if instance.user_type == "Sales + Marketing Person":
            Admin.objects.create(users=instance)
        

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "Admin":
        instance.admin.save()
    if instance.user_type == "Operation Person":
        instance.admin.save()
    if instance.user_type == "Sales Person":
        instance.admin.save()
    if instance.user_type == "Hotel Reservation Person":
        instance.admin.save()
    if instance.user_type == "Visa Service":
        instance.admin.save()
    if instance.user_type == "Account":
        instance.admin.save()
    if instance.user_type == "Ground Operation":
        instance.admin.save()
    if instance.user_type == "Hr":
        instance.admin.save()
    if instance.user_type == "Customer Service":
        instance.admin.save()
    if instance.user_type == "Marketing Person":
        instance.admin.save()
    if instance.user_type == "Sales + Marketing Person":
        instance.admin.save()


    
    
from django.contrib import admin
from .models import *
# from import_export.admin import ImportExportActionModelAdmin,ImportExportModelAdmin
from .resources import LeadResource


class LeadAdmin(admin.ModelAdmin):
    resource_class = LeadResource
    model = Lead
    list_display = [ "enquiry_number","name", "email", "mobile_number"]



admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(Meal_Plan)
admin.site.register(Hotel_Category)
admin.site.register(Ferry_Class)
admin.site.register(Expense_servive_type)
admin.site.register(Extra_Meal_Price)
admin.site.register(Flight)
admin.site.register(Currency)
admin.site.register(Lead_source)
admin.site.register(Bank)
admin.site.register(Destination)
admin.site.register(Restaurent_location)
admin.site.register(Restaurent_type)
admin.site.register(Special_days)
admin.site.register(Room_type)
admin.site.register(Hotel_location)
admin.site.register(Amenities)
admin.site.register(Arrival_Departure)
admin.site.register(Visa)
admin.site.register(Transfer_location)
admin.site.register(Guide)
admin.site.register(Restaurent)
admin.site.register(Hotel)
admin.site.register(ExtraMeal)
admin.site.register(Day)
admin.site.register(Sightseeing)
admin.site.register(Supplier)
admin.site.register(Transfer)
admin.site.register(Service_type)
admin.site.register(Itinerary)
admin.site.register(Document)
admin.site.register(Folder)
admin.site.register(Role_Permission)
admin.site.register(CustomUser)
admin.site.register(Admin)
admin.site.register(Lead,LeadAdmin)
admin.site.register(Quatation)
admin.site.register(Attachment)
admin.site.register(Notes)
admin.site.register(Payment)
admin.site.register(Followup)
admin.site.register(ActivityHistory)
admin.site.register(File)
admin.site.register(ConfirmAttachment)
admin.site.register(Messages)
admin.site.register(BookingCard)
admin.site.register(Notification)
admin.site.register(PaymentAttachment)
admin.site.register(TicketingQuery)
admin.site.register(PersonalDetail)
from django.contrib import admin
from .models import *
# from import_export.admin import ImportExportActionModelAdmin,ImportExportModelAdmin
from .resources import LeadResource
from import_export.admin import ImportExportModelAdmin,ExportMixin
from import_export.resources import ModelResource
class LeadResource(ModelResource):
    class Meta:
        model = Lead  # Link resource to Lead model
        # import_id_fields = ('id',)  # Ensure ID field is used for import
        def dehydrate_countrys(self, lead):
            return lead.countrys.country_name if lead.countrys else ""
        def dehydrate_destinations(self, lead):
            return lead.destinations.name if lead.destinations else ""
        def dehydrate_service_type(self, lead):
            return lead.service_type.name if lead.service_type else ""
        def dehydrate_lead_source(self, lead):
            return lead.lead_source.name if lead.lead_source else ""
        def dehydrate_operation_person(self, lead):
            return lead.operation_person.username if lead.operation_person else ""
        def dehydrate_sales_person(self, lead):
            return lead.sales_person.username if lead.sales_person else ""


# class LeadAdmin(ImportExportModelAdmin,admin.ModelAdmin):
#     resource_class = LeadResource
#     model = Lead
#     list_display = [ "enquiry_number","lead_status","name", "email", "mobile_number","date"]
#     search_fields = ['enquiry_number', 'name', 'email', 'mobile_number', 'date']
#     list_filter = ('lead_status', 'date','email')
#     def get_export_queryset(self, request):
#         qs = super().get_export_queryset(request)
#         # ✅ Admin panel me filter apply ho to sirf wahi data export hoga
#         if 'lead_status' in request.GET:
#             return qs.filter(lead_status=request.GET['lead_status'])
#         return qs

class LeadAdmin(ImportExportModelAdmin, ExportMixin):  
    resource_class = LeadResource  
    model = Lead

    # ✅ Foreign Key fields ke readable names ko display karega
    list_display = [
        "enquiry_number", "lead_status", "name", "email", "mobile_number", 
        "get_country", "get_destination", "get_service", "get_lead_source", "date"
    ]
    
    search_fields = ['enquiry_number', 'name', 'email', 'mobile_number', 'date']
    list_filter = ('lead_status', 'date', 'email')

    # ✅ Foreign Key fields ke readable names ke liye methods
    def get_country(self, obj):
        return obj.countrys.country_name if obj.countrys else ""
    get_country.admin_order_field = 'countrys'  
    get_country.short_description = 'Country'

    def get_destination(self, obj):
        return obj.destinations.name if obj.destinations else ""
    get_destination.admin_order_field = 'destinations'
    get_destination.short_description = 'Destination'

    def get_service(self, obj):
        return obj.service_type.name if obj.service_type else ""
    get_service.admin_order_field = 'service_type'
    get_service.short_description = 'Service Type'

    def get_lead_source(self, obj):
        return obj.lead_source.name if obj.lead_source else ""
    get_lead_source.admin_order_field = 'lead_source'
    get_lead_source.short_description = 'Lead Source'

# 
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
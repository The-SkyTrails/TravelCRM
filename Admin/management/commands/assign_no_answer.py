# from django.core.management.base import BaseCommand
# from Admin.models import CustomUser, Lead  # your_app ko apne app name se replace karein

# class Command(BaseCommand):
#     help = 'Assigns "Connected" leads to Dummy2 (yomor66005@gmail.com)'

#     def handle(self, *args, **kwargs):
#         try:
#             # "Dummy2" user fetch karein
#             user = CustomUser.objects.get(username="yomor66005@gmail.com", user_type="Sales Person")
#         except CustomUser.DoesNotExist:
#             self.stdout.write(self.style.ERROR("User 'Dummy2' not found!"))
#             return

#         # "No Answer" wale leads ko assign karein
#         updated_count = Lead.objects.filter(lead_status="Quotation Send").update(sales_person=user)

#         if updated_count > 0:
#             self.stdout.write(self.style.SUCCESS(f"Successfully updated {updated_count} leads!"))
#         else:
#             self.stdout.write(self.style.WARNING("No leads found with status 'No Answer'"))



from django.core.management.base import BaseCommand
from Admin.models import CustomUser, Lead
from random import sample

class Command(BaseCommand):
    help = 'Randomly assigns 50-50 leads to Gaurav and Imran from Dummy2 with status Pending'

    def handle(self, *args, **kwargs):
        try:
            # Users fetch karo
            dummy_user = CustomUser.objects.get(username="yomor66005@gmail.com", user_type="Sales Person")
            gaurav_user = CustomUser.objects.get(username="gaurav@theskytrails.com", user_type="Sales Person")
            imran_user = CustomUser.objects.get(username="imran@theskytrails.com", user_type="Sales Person")
        except CustomUser.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f"User not found: {str(e)}"))
            return

        # Dummy user wali 2041 leads fetch karo
        leads_queryset = Lead.objects.filter(sales_person=dummy_user)

        # Agar 100 se kam lead hai to error do
        if leads_queryset.count() < 100:
            self.stdout.write(self.style.WARNING("Not enough leads to reassign 50-50"))
            return

        # Random 100 leads chuno
        random_leads = sample(list(leads_queryset), 100)

        # First 50 leads Gaurav ko
        for lead in random_leads[:50]:
            lead.sales_person = gaurav_user
            lead.lead_status = "Pending"
            lead.save()

        # Next 50 leads Imran ko
        for lead in random_leads[50:]:
            lead.sales_person = imran_user
            lead.lead_status = "Pending"
            lead.save()

        self.stdout.write(self.style.SUCCESS("Successfully assigned 50-50 leads with 'Pending' status."))


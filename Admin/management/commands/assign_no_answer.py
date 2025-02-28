from django.core.management.base import BaseCommand
from Admin.models import CustomUser, Lead  # your_app ko apne app name se replace karein

class Command(BaseCommand):
    help = 'Assigns "No Answer" leads to Dummy2 (yomor66005@gmail.com)'

    def handle(self, *args, **kwargs):
        try:
            # "Dummy2" user fetch karein
            user = CustomUser.objects.get(username="yomor66005@gmail.com", user_type="Sales Person")
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR("User 'Dummy2' not found!"))
            return

        # "No Answer" wale leads ko assign karein
        updated_count = Lead.objects.filter(lead_status="No Answer").update(sales_person=user)

        if updated_count > 0:
            self.stdout.write(self.style.SUCCESS(f"Successfully updated {updated_count} leads!"))
        else:
            self.stdout.write(self.style.WARNING("No leads found with status 'No Answer'"))

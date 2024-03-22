from datetime import date
from .models import Followup  


def followups_due_today(request):
    today = date.today()
    followups_due_today = Followup.objects.filter(date=today)
    return {'followups_due_today': followups_due_today}
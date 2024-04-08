from datetime import date
from .models import Followup  
from django.db.models import Q

def followups_due_today(request):
    today = date.today()
    followups_due_today = Followup.objects.none()  
    
    if request.user.is_authenticated:
        if request.user == "Admin":  
            followups_due_today = Followup.objects.filter(date=today)
        else:
            followups_due_today = Followup.objects.filter(
                Q(lead__added_by=request.user) | Q(lead__sales_person=request.user),
                date=today
            )
    
    return {'followups_due_today': followups_due_today}


from datetime import date
from .models import Followup  
from django.db.models import Q

def followups_due_today(request):
    today = date.today()
    followups_due_today = Followup.objects.none()  
    
    if request.user.is_authenticated:
        if request.user == "Admin":  
            followups_due_today = Followup.objects.filter(date=today)
        else:
            followups_due_today = Followup.objects.filter(
                Q(lead__added_by=request.user) | Q(lead__sales_person=request.user),
                date=today
            )
    
    return {'followups_due_today': followups_due_today}


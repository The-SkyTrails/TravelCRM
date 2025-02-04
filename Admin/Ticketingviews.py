from django.shortcuts import render, HttpResponse, redirect, get_object_or_404 , reverse
from .models import TicketingQuery
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def ticketingindex(request): 
    tickets_query = TicketingQuery.objects.filter(ticketing_user = request.user).order_by('-id')[:10]
    Count_tickets_query = TicketingQuery.objects.filter(ticketing_user = request.user).count()
    
    context = {
        "tickets_query":tickets_query,
        "Count_tickets_query":Count_tickets_query
    }
    return render(request,"Ticketing/Base/index2.html",context)



def ticketing_queries(request):
    tickets_query = TicketingQuery.objects.filter(ticketing_user = request.user)
    paginator = Paginator(tickets_query, 10)
    page_number = request.GET.get('page')
    

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {
        "tickets_query":tickets_query,
        "page":page
    }
    return render(request, "Ticketing/Query/query_list.html",context)


def update_tkt_status(request,id):
    tkt = TicketingQuery.objects.get(id=id)
    if request.method == "POST":
        tkt_status = request.POST.get("tkt_status")
        tkt.status = tkt_status
        tkt.save()
        return redirect("ticketing_queries")



from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

@csrf_exempt
def facebook_webhook(request):
    VERIFY_TOKEN = "demootestings"  # Set the same Verify Token as in Facebook

    if request.method == "GET":
        # Facebook Webhook Verification
        mode = request.GET.get("hub.mode")
        challenge = request.GET.get("hub.challenge")
        verify_token = request.GET.get("hub.verify_token")

        print(f"Mode: {mode}, Verify Token: {verify_token}, Challenge: {challenge}")

        if mode == "subscribe" and verify_token == VERIFY_TOKEN:
            return JsonResponse({"hub.challenge": challenge})  # Return the challenge
        else:
            return JsonResponse({"error": "Invalid token or mode"}, status=403)

    elif request.method == "POST":
        # Handle Incoming Lead Data
        try:
            data = json.loads(request.body)
            print("Received Lead Data:", json.dumps(data, indent=4))  # Log data for debugging
            return JsonResponse({"message": "Lead received successfully!"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

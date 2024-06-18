from django.shortcuts import render, HttpResponse, redirect, get_object_or_404 , reverse
from .models import *
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import requests
from datetime import datetime
import json
from django.core.mail import EmailMessage
import mimetypes 
import uuid
from django.db.models import Q
from .tatatele_api.call_records import fetch_recording_urls_and_dates,LeadWiseCallRecords
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import csv
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMultiAlternatives
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@login_required
def accountindex(request):  
    return render(request,"Account/Base/index2.html")


@login_required
def paymentreceivelist(request):
    context = {} 
    
    all_lead = Lead.objects.filter(account_person=request.user).order_by("-last_updated_at")
    
    for lead in all_lead:
        lead.payment_approved = PaymentAttachment.objects.filter(lead=lead, status=True).exists()
    
    
    paginator = Paginator(all_lead,10)
    page_number = request.GET.get('page')
    

    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        
        "page":page,
    }
    
    return render(request,"Account/Query/paymentreceive.html",context)


@login_required
def approvepayment(request,id):
    lead_instance = get_object_or_404(Lead, id=id)

    payment_attachments = PaymentAttachment.objects.filter(lead=lead_instance)

    payment_attachments.update(status=True)

    return redirect("paymentreceivelist")
    



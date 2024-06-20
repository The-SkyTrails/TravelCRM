from django.shortcuts import render, HttpResponse, redirect, get_object_or_404 , reverse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@login_required
def accountindex(request): 
    context = {}  
    paymentattachments = PaymentAttachment.objects.filter(status = False).order_by("-created_at")
    approvedpayment = PaymentAttachment.objects.filter(status = True).order_by("-created_at")
    
    context = {
        "paymentattachments":paymentattachments,
        "approvedpayment":approvedpayment
    }
    
    return render(request,"Account/Base/index2.html",context)


@login_required
def paymentreceivelist(request):
    context = {} 
    paymentattachments = PaymentAttachment.objects.filter(status = False).order_by("-created_at")
    approvedpayment = PaymentAttachment.objects.filter(status = True).order_by("-created_at")
    
    paginator = Paginator(paymentattachments,100)
    page_number = request.GET.get('page')
    

    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        
        "page":page,
        "paymentattachments":paymentattachments,
        "approvedpayment":approvedpayment
        
    }
    
    return render(request,"Account/Query/paymentreceive.html",context)

@login_required
def approvepaymentlist(request):
    context = {} 
    approvedpayment = PaymentAttachment.objects.filter(status = True).order_by("-created_at")
    paymentattachments = PaymentAttachment.objects.filter(status = False).order_by("-created_at")
    
    # for lead in approvedpayment:
    #     lead.payment_approved = PaymentAttachment.objects.filter(lead=lead, status=True).exists()
    
    paginator = Paginator(approvedpayment,100)
    page_number = request.GET.get('page')
    

    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        
        "page":page,
        "paymentattachments":paymentattachments,
        "approvedpayment":approvedpayment
    }
    
    return render(request,"Account/Query/approvepayment.html",context)

@login_required
def approvepayment(request, id):
    payment_attachment = get_object_or_404(PaymentAttachment, id=id)
    lead_instance = payment_attachment.lead

    payment_attachment.status = True
    payment_attachment.save()

    payment_attachments = PaymentAttachment.objects.filter(lead=lead_instance, status=True)
    total_amount = sum(float(pa.amount) for pa in payment_attachments)

    complete_package_cost = float(lead_instance.complete_package_cost)  
    balance_package_cost = complete_package_cost - total_amount
    lead_instance.balance_package_cost = balance_package_cost

    lead_instance.received_package_cost = total_amount
    lead_instance.save()

    return redirect("paymentreceivelist")
    
@login_required
def add_notes(request, id):
    if request.method == "POST":
        enq = request.POST.get("enq_id")
        notes = request.POST.get("notes")
        
        try:
            payment_attachment = get_object_or_404(PaymentAttachment, id=enq)
            lead_instance = payment_attachment.lead
            note = Notes.objects.create(lead=lead_instance,notes=notes)
            activity_history = ActivityHistory.objects.create(lead=lead_instance, activity_type='Note')
            note.activity = activity_history
            lead_instance.last_updated_at = timezone.now()
            lead_instance.save()
            note.save()


            messages.success(request, "Note Added Successfully...")
        except Lead.DoesNotExist:
            pass
        
        return redirect("paymentreceivelist")
    else:
        pass
    
    
@login_required   
def account_view_booking_cards(request, id):
    payment_attachment = get_object_or_404(PaymentAttachment, id=id)
    lead_instance = payment_attachment.lead
    booking_cards = lead_instance.bookingcard_set.all()
    
    context = {
        'payment_attachment': payment_attachment,
        'booking_cards': booking_cards,
        'lead_instance':lead_instance
    }
    return render(request, 'Account/Query/viewbookingcard.html', context)
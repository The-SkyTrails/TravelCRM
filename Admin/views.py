from django.shortcuts import render, HttpResponse, redirect, get_object_or_404 , reverse
from .models import *
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import requests
from datetime import date
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


@login_required
def index(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type  
        if user_type == "Admin":
            all_lead = Lead.objects.all().order_by("-id")
            quatation_lead_list = Lead.objects.filter(lead_status="Quotation Send").order_by("-id")
            comlead_list = Lead.objects.filter(lead_status="Completed").order_by("-id")
            lost_list = Lead.objects.filter(lead_status="Lost").order_by("-id")
            follow_up = Followup.objects.all().order_by('-id')[:10]
        elif user_type == "Sales Person":
            all_lead = Lead.objects.filter(Q(added_by=request.user) | Q(sales_person=request.user)).order_by("-id")
            quatation_lead_list = Lead.objects.filter(Q(lead_status="Quotation Send") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            comlead_list = Lead.objects.filter(lead_status="Completed").order_by("-id")
            lost_list = Lead.objects.filter(lead_status="Lost").order_by("-id")
            follow_up = Followup.objects.filter(Q(lead__added_by=request.user) | Q(lead__sales_person=request.user)).order_by('-id')[:10]
        else:
            pass
        
        context = {
        "quatation_lead_list": quatation_lead_list,
        "comlead_list": comlead_list,
        "all_lead": all_lead,
        "lost_list": lost_list,
        "follow_up":follow_up
    }
    return render(request,"Admin/Base/index2.html", context)

@login_required
def add_Country(request):

    country_list = Country.objects.all()

    context = {
        "country_list": country_list,
        "message": "Country Deleted Successfully!!!",
    }

    return render(request, "Admin/Country/add_country.html", context)


def country(request):

    country_list = Country.objects.all()
    if request.method == "POST":

        country_name = request.POST.get("country_name").capitalize()
        sort_name = request.POST.get("sort_name").capitalize()
        nationality = request.POST.get("nationality").capitalize()

        if Country.objects.filter(country_name=country_name):
            return HttpResponseBadRequest("WRONG")
        country = Country.objects.create(
            country_name=country_name, sort_name=sort_name, nationality=nationality
        )
        country.save()
    context = {"country_list": country_list}

    return render(request, "Admin/Country/country-list.html", context)


def check_country(request):
    country_name = request.POST.get("country_name").capitalize()
    if Country.objects.filter(country_name=country_name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Country Name already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Country name is available</div>"
        )


def edit_Country(request, id):
    if request.method == "POST": 
        try:
            country_name = request.POST.get("country_name").capitalize()
            nationality = request.POST.get("nationality").capitalize()
            sort_name = request.POST.get("sort_name").capitalize()
            country = Country.objects.get(id=id)
            country.country_name = country_name
            country.nationality = nationality
            country.sort_name = sort_name
            country.save()
            messages.success(request, "Country updated successfully")
            return redirect("add_Country")
        except Exception as e:
                messages.error(request, f"Error occurred: {e}")
                return redirect("add_Country")
    else:
        pass
    

    return render(request, "Admin/Country/add_country.html")


def delete_country(request, id):
    con = Country.objects.get(id=id)
    con.delete()
    messages.success(request, "Country Deleted log for alertify!!!")
    return redirect("add_Country")


# --------------------------------- State --------------------------

@login_required
def state(request):
    state_list = State.objects.all()
    country = Country.objects.all()
    context = {
        "state_list": state_list,
        "message": "State Deleted Successfully!!!",
        "country": country
        
    }

    return render(request, "Admin/State/state.html", context)

@login_required
def addstate(request):

    state_list = State.objects.all()
    country = Country.objects.all()
    
    if request.method == "POST":

        state_name = request.POST.get("state_name").capitalize()
        countryid = request.POST.get("country_id").capitalize()

        if State.objects.filter(name=state_name):
            return HttpResponseBadRequest("WRONG")
        contry = Country.objects.get(id=countryid)
        state = State.objects.create(name=state_name, country=contry)
        state.save()
    context = {"state_list": state_list,"country": country,}

    return render(request, "Admin/State/state.html", context)


def check_state(request):
    state_name = request.POST.get("state_name").capitalize()
    if State.objects.filter(name=state_name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>State Name already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>State name is available</div>"
        )

def editstate(request, id):
    if request.method == "POST":
        try:
            state_name = request.POST.get("state_name").capitalize()
            country_id = request.POST.get("country_id").capitalize()
            country = Country.objects.get(id=country_id)
            state = State.objects.get(id=id)
            state.country = country
            state.name = state_name
            state.save()
            messages.success(request, "State updated successfully")
            return redirect("addstate")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("addstate")
    else:
        pass
    

    return render(request, "Admin/State/state.html")



def delete_state(request, id):
    state = State.objects.get(id=id)
    state.delete()
    return redirect("state")



# ------------------------------------ CITY -----------------------


def checkcity(request): 
    city_name = request.POST.get("city_name").capitalize()
    if City.objects.filter(name=city_name):
        return HttpResponse(
            "<div id='post-data-container2' class='error mx-2'>City Name already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container2' class='success'>City name is available</div>"
        )

@login_required
def city(request):
    state = State.objects.all()
    city_list = City.objects.all()
    context = {
        "city_list": city_list,
        "message": "City Deleted Successfully!!!",
        "state": state,
    }

    return render(request, "Admin/City/city.html", context)

@login_required
def addcity(request):
    state = State.objects.all()
    city_list = City.objects.all()

    if request.method == "POST":

        city_name = request.POST.get("city_name").capitalize()
        state_id = request.POST.get("state_id")
    
        if City.objects.filter(name=city_name):

            message = "City already exists"
            return HttpResponseBadRequest(message)
        statee = State.objects.get(id=state_id)
        city = City.objects.create(name=city_name, state=statee)
        city.save()
        
    context = {"city_list": city_list,"state":state}

    return render(request, "Admin/City/city.html", context)


def editcity(request, id):
    if request.method == "POST":
        try:
            city_name = request.POST.get("city_name").capitalize()
            state_id = request.POST.get("state_id")
            state = State.objects.get(id=state_id)
            city = City.objects.get(id=id)
            city.name = city_name
            city.state = state
            city.save()
            messages.success(request, "City updated successfully")
            return redirect("city")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("city")
    else:
        pass
            
    city_list = City.objects.all()
    context = {
        "city_list": city_list,
    }

    return render(request, "Admin/City/city.html", context)


def delete_city(request, id):
    city = City.objects.get(id=id)
    city.delete()
    return redirect("city")


# ----------------------------------------------------------------------

@login_required
def add_vehicle(request):

    vehicle_list = Vehicle.objects.all()
    context = {
        "vehicle_list": vehicle_list,
        "message": "vehicle Deleted Successfully!!!",
    }

    return render(request, "Admin/Vehicle/add_vehicle.html", context)

@login_required
def vehicle(request):

    vehicle_list = Vehicle.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        brand = request.POST.get("brand").capitalize()
        sightseeing_capacity = request.POST.get("sightseeing_capacity").capitalize()
        transfer_capacity = request.POST.get("transfer_capacity").capitalize()
        image = request.FILES.get("image")

        try:

            vehicle = Vehicle.objects.create(
                name=name,
                brand=brand,
                sightseeing_capacity=sightseeing_capacity,
                transfer_capacity=transfer_capacity,
                image=image,
            )
            vehicle.save()
            return HttpResponse("Vehicle created successfully!")

        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {str(e)}")
    context = {"vehicle_list": vehicle_list}

    return render(request, "Admin/Vehicle/vehicle-list.html", context)


def edit_vehicle(request, id):
    if request.method == "POST":
        try:

            name = request.POST.get("name").capitalize()
            brand = request.POST.get("brand").capitalize()
            sightseeing_capacity = request.POST.get("sightseeing_capacity").capitalize()
            transfer_capacity = request.POST.get("transfer_capacity").capitalize()
            image = request.FILES.get("image")
            vehicle = Vehicle.objects.get(id=id)
            vehicle.name = name
            vehicle.brand = brand
            vehicle.sightseeing_capacity = sightseeing_capacity
            vehicle.transfer_capacity = transfer_capacity
            if image:
                vehicle.image = image
            vehicle.save()
            messages.success(request, "Vehicle updated successfully")
            return redirect("add_vehicle")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_vehicle")
    else:
        pass

    vehicle_list = Vehicle.objects.all()
    context = {
        "vehicle_list": vehicle_list,
        "message": "Vehicle Deleted Successfully!!!",
    }

    return render(request, "Admin/Vehicle/add_vehicle.html", context)


def delete_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)
    vehicle.delete()
    messages.success(request, "Vehicle Deleted log for alertify!!!")
    return redirect("add_vehicle")
# ----------------------------------------------------------------------

@login_required
def add_driver(request):

    driver_list = Driver.objects.all()
    vechicle = Vehicle.objects.all()

    context = {
        "driver_list": driver_list,
        "message": "Driver Deleted Successfully!!!",
        "vechicle": vechicle,
    }

    return render(request, "Admin/Driver/add_driver.html", context)

@login_required
def driver(request):

    driver_list = Driver.objects.all()

    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        code = request.POST.get("code")
        mobile = request.POST.get("mobile")
        alternate_no = request.POST.get("alternate_no")
        passport = request.POST.get("passport")
        vehicle = request.POST.get("vehicle")
        address = request.POST.get("address")
        car_image = request.FILES.get("car_image")
        licence_image = request.FILES.get("licence_image")
        vehicle_id = Vehicle.objects.get(id=vehicle)
        
        driver = Driver.objects.create(
            name=name,
            code=code,
            mobile=mobile,
            alternate_no=alternate_no,
            passport=passport,
            vehicle=vehicle_id,
            address=address,
            car_image=car_image,
            licence_image=licence_image,
        )

        driver.save()

        return HttpResponse("Driver created successfully!")

    context = {"driver_list": driver_list}

    return render(request, "Admin/Driver/driver-list.html", context)


def edit_driver(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            code = request.POST.get("code")
            mobile = request.POST.get("mobile")
            alternate_no = request.POST.get("alternate_no")
            passport = request.POST.get("passport")
            vehicle_id = request.POST.get("vehicle")
            address = request.POST.get("address")
            car_image = request.FILES.get("car_image")
            licence_image = request.FILES.get("licence_image")

            vehicle = Vehicle.objects.get(id=vehicle_id)
            driver = Driver.objects.get(id=id)
            driver.name = name
            driver.code = code
            driver.mobile = mobile
            driver.alternate_no = alternate_no
            driver.passport = passport
            driver.vehicle = vehicle
            driver.address = address

            if car_image:
                driver.car_image = car_image
            if licence_image:
                driver.licence_image = licence_image

            driver.save()
            messages.success(request, "Driver updated successfully")
            return redirect("add_driver")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_driver")
    else:
        pass

    return render(request, "Admin/Driver/add_driver.html")


def get_transfer_capacity(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        return JsonResponse({"transfer_capacity": vehicle.transfer_capacity})
    except Vehicle.DoesNotExist:
        return JsonResponse({"error": "Vehicle not found"}, status=404)


def delete_driver(request, id):
    driver = Driver.objects.get(id=id)
    driver.delete()
    messages.success(request, "Driver Deleted log for alertify!!!")
    return redirect("add_driver")

# ----------------------------- Meal Plan ------------------------------------


@login_required
def add_meal_plan(request):

    meal_plan_list = Meal_Plan.objects.all()

    context = {
        "meal_plan_list": meal_plan_list,
        "message": "Meal Plan Deleted Successfully!!!",
    }

    return render(request, "Admin/MealPlan/add_meal_plan.html", context)

@login_required
def meal_plan(request):

    meal_plan_list = Meal_Plan.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Meal_Plan.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        meal_plan = Meal_Plan.objects.create(name=name)
        meal_plan.save()
    context = {"meal_plan_list": meal_plan_list}

    return render(request, "Admin/MealPlan/meal-list.html", context)


def check_meal_plan(request):
    name = request.POST.get("name").capitalize()
    if Meal_Plan.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Meal Plan Name already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Meal Plan name is available</div>"
        )


def edit_meal_plan(request, id):
    if request.method == "POST":
        try:

            name = request.POST.get("name").capitalize()
            meal_plan = Meal_Plan.objects.get(id=id)
            meal_plan.name = name
            meal_plan.save()
            messages.success(request, "Meal Plan updated successfully")
            return redirect("add_meal_plan")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_meal_plan")
    else:
        pass
    meal_plan_list = Meal_Plan.objects.all()
    context = {
        "meal_plan_list": meal_plan_list,
        "message": "Meal Plan Deleted Successfully!!!",
    }

    return render(request, "Admin/MealPlan/add_meal_plan.html", context)


def delete_meal_plan(request, id):
    meal_plan = Meal_Plan.objects.get(id=id)
    meal_plan.delete()
    messages.success(request, "Meal Plan Deleted log for alertify!!!")
    return redirect("add_meal_plan")

# ----------------------------- Hotel Category ------------------------------------

@login_required
def add_hotel_category(request):

    hotel_category_list = Hotel_Category.objects.all()

    context = {
        "hotel_category_list": hotel_category_list,
        "message": "Hotel Category Deleted Successfully!!!",
    }

    return render(request, "Admin/HotelCategory/add_hotel_category.html", context)

@login_required
def hotel_category(request):

    hotel_category_list = Hotel_Category.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Hotel_Category.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        hotel_category = Hotel_Category.objects.create(name=name)
        hotel_category.save()
    context = {"hotel_category_list": hotel_category_list}

    return render(request, "Admin/HotelCategory/hotel_category-list.html", context)


def check_hotel_category(request):
    name = request.POST.get("name").capitalize()
    if Hotel_Category.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Hotel Category already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Hotel Category is available</div>"
        )


def edit_hotel_category(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            hotel_category = Hotel_Category.objects.get(id=id)
            hotel_category.name = name
            hotel_category.save()
            messages.success(request, "Hotel Category updated successfully")
            return redirect("add_hotel_category")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_hotel_category")
    else:
        pass
    hotel_category_list = Hotel_Category.objects.all()
    context = {
        "hotel_category_list": hotel_category_list,
        "message": "Hotel Category Deleted Successfully!!!",
    }

    return render(request, "Admin/HotelCategory/add_hotel_category.html", context)


def delete_hotel_category(request, id):
    hotel_category = Hotel_Category.objects.get(id=id)
    hotel_category.delete()
    messages.success(request, "Hotel Category Deleted log for alertify!!!")
    return redirect("add_hotel_category")

# ----------------------------- Ferry Class ------------------------------------

@login_required
def add_ferry_class(request):

    ferry_class_list = Ferry_Class.objects.all()

    context = {
        "ferry_class_list": ferry_class_list,
        "message": "Ferry Class Deleted Successfully!!!",
    }

    return render(request, "Admin/FerryClass/add_ferry_class.html", context)

@login_required
def ferry_class(request):

    ferry_class_list = Ferry_Class.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Ferry_Class.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        ferry_class = Ferry_Class.objects.create(name=name)
        ferry_class.save()
    context = {"ferry_class_list": ferry_class_list}

    return render(request, "Admin/FerryClass/ferry_class-list.html", context)


def check_ferry_class(request):
    name = request.POST.get("name").capitalize()
    if Ferry_Class.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Ferry Class already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Ferry Class is available</div>"
        )


def edit_ferry_class(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            ferry_class = Ferry_Class.objects.get(id=id)
            ferry_class.name = name
            ferry_class.save()
            messages.success(request, "Ferry Class updated successfully")
            return redirect("add_ferry_class")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_ferry_class")
    else:
        pass
    ferry_class_list = Ferry_Class.objects.all()
    context = {
        "ferry_class_list": ferry_class_list,
        "message": "Ferry Class Deleted Successfully!!!",
    }

    return render(request, "Admin/FerryClass/add_ferry_class.html", context)


def delete_ferry_class(request, id):
    ferry_class = Ferry_Class.objects.get(id=id)
    ferry_class.delete()
    messages.success(request, "Ferry Class Deleted log for alertify!!!")
    return redirect("add_ferry_class")

# ----------------------------- Extra Expense Type ------------------------------------

@login_required
def add_extra_service(request):

    extra_service_list = Service_type.objects.all()

    context = {
        "extra_service_list": extra_service_list,
        "message": "Extra Service Type Deleted Successfully!!!",
    }

    return render(request, "Admin/ExtraServiceType/add_extra_service.html", context)

@login_required
def extra_service(request):

    extra_service_list = Service_type.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        remarks = request.POST.get("remarks")

        if Service_type.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        extra_service = Service_type.objects.create(name=name, remarks=remarks)
        extra_service.save()
    context = {"extra_service_list": extra_service_list}

    return render(request, "Admin/ExtraServiceType/extra_service-list.html", context)


def check_extra_service(request):
    name = request.POST.get("name").capitalize()
    if Service_type.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Extra Service Type already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Extra Service Type is available</div>"
        )


def edit_extra_service(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            remarks = request.POST.get("remarks")
            extra_service = Service_type.objects.get(id=id)
            extra_service.name = name
            extra_service.remarks = remarks
            extra_service.save()
            messages.success(request, "Extra Service Type updated successfully")
            return redirect("add_extra_service")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_extra_service")
    else:
        pass
    extra_service_list = Service_type.objects.all()
    context = {
        "extra_service_list": extra_service_list,
        "message": "Extra Service Type Deleted Successfully!!!",
    }

    return render(request, "Admin/ExtraServiceType/add_extra_service.html", context)



def delete_extra_service(request, id):
    extra_service = Service_type.objects.get(id=id)
    extra_service.delete()
    messages.success(request, "Extra Service Type Deleted log for alertify!!!")
    return redirect("add_extra_service")

# ----------------------------- Extra Meal Price ------------------------------------

@login_required
def add_extra_meal_price(request):

    extra_meal_price_list = Extra_Meal_Price.objects.all()

    context = {
        "extra_meal_price_list": extra_meal_price_list,
        "message": "Extra Meal Price Deleted Successfully!!!",
    }

    return render(request, "Admin/ExtraMealPrice/add_extra_meal_price.html", context)

@login_required
def extra_meal_price(request):

    extra_meal_price_list = Extra_Meal_Price.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        adult = request.POST.get("adult")
        child = request.POST.get("child")
        infant = request.POST.get("infant")

        if Extra_Meal_Price.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        extra_meal_price = Extra_Meal_Price.objects.create(
            name=name, adult=adult, child=child, infant=infant
        )
        extra_meal_price.save()
    context = {"extra_meal_price_list": extra_meal_price_list}

    return render(request, "Admin/ExtraMealPrice/extra_meal_price-list.html", context)


def check_extra_meal_price(request):
    name = request.POST.get("name").capitalize()
    if Extra_Meal_Price.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Extra Meal Price already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Extra Meal Price is available</div>"
        )


def edit_extra_meal_price(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            adult = request.POST.get("adult")
            child = request.POST.get("child")
            infant = request.POST.get("infant")
            extra_meal_price = Extra_Meal_Price.objects.get(id=id)
            extra_meal_price.name = name
            extra_meal_price.adult = adult
            extra_meal_price.child = child
            extra_meal_price.infant = infant
            extra_meal_price.save()
            messages.success(request, "Extra Meal Price updated successfully")
            return redirect("add_extra_meal_price")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_extra_meal_price")
    else:
        pass
    extra_meal_price_list = Extra_Meal_Price.objects.all()
    context = {
        "extra_meal_price_list": extra_meal_price_list,
        "message": "Extra Meal Price Deleted Successfully!!!",
    }

    return render(request, "Admin/ExtraMealPrice/add_extra_meal_price.html", context)


def delete_extra_meal_price(request, id):
    extra_meal_price = Extra_Meal_Price.objects.get(id=id)
    extra_meal_price.delete()
    messages.success(request, "Extra Meal Price Deleted log for alertify!!!")
    return redirect("add_extra_meal_price")


# ----------------------------- Flight ------------------------------------

@login_required
def add_flight(request):

    flight_list = Flight.objects.all()

    context = {
        "flight_list": flight_list,
        "message": "Flight Deleted Successfully!!!",
    }

    return render(request, "Admin/Flight/add_flight.html", context)

@login_required
def flight(request):

    flight_list = Flight.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        image = request.FILES.get("image")

        if Flight.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        flight = Flight.objects.create(name=name, image=image)
        flight.save()
    context = {"flight_list": flight_list}

    return render(request, "Admin/Flight/flight-list.html", context)


def check_flight(request):
    name = request.POST.get("name").capitalize()
    if Flight.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Flight already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Flight is available</div>"
        )


def edit_flight(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            image = request.FILES.get("image")
            flight = Flight.objects.get(id=id)
            flight.name = name
            if image:
                flight.image = image
            flight.save()
            messages.success(request, "Flight updated successfully")
            return redirect("add_flight")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_flight")
    else:
        pass
    flight_list = Flight.objects.all()
    context = {
        "flight_list": flight_list,
        "message": "Flight Deleted Successfully!!!",
    }

    return render(request, "Admin/Flight/add_flight.html", context)


def delete_flight(request, id):
    flight = Flight.objects.get(id=id)
    flight.delete()
    messages.success(request, "Flight Deleted log for alertify!!!")
    return redirect("add_flight")

# ----------------------------- Currency ------------------------------------

@login_required
def add_currency(request):

    currency_list = Currency.objects.all()

    context = {
        "currency_list": currency_list,
        "message": "Currency Deleted Successfully!!!",
    }

    return render(request, "Admin/Currency/add_currency.html", context)

@login_required
def currency(request):

    currency_list = Currency.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        value = request.POST.get("value")
        base_currency = request.POST.get("base_currency")

        if Currency.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        currency = Currency.objects.create(
            name=name, value=value, base_currency=base_currency
        )
        currency.save()
    context = {"currency_list": currency_list}

    return render(request, "Admin/Currency/currency-list.html", context)


def check_currency(request):
    name = request.POST.get("name").capitalize()
    if Currency.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Currency already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Currency is available</div>"
        )


def edit_currency(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            value = request.POST.get("value")
            base_currency = request.POST.get("base_currency")
            currency = Currency.objects.get(id=id)
            currency.name = name
            currency.value = value
            currency.base_currency = base_currency
            currency.save()
            messages.success(request, "Currency updated successfully")
            return redirect("add_currency")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_currency")
    else:
        pass
    currency_list = Currency.objects.all()
    context = {
        "currency_list": currency_list,
        "message": "Currency Deleted Successfully!!!",
    }

    return render(request, "Admin/Currency/add_currency.html", context)


def delete_currency(request, id):
    currency = Currency.objects.get(id=id)
    currency.delete()
    messages.success(request, "Currency Deleted log for alertify!!!")
    return redirect("add_currency")

# ----------------------------- Lead Source ------------------------------------

@login_required
def add_lead_source(request):

    lead_source_list = Lead_source.objects.all()

    context = {
        "lead_source_list": lead_source_list,
        "message": "Lead Source Deleted Successfully!!!",
    }

    return render(request, "Admin/LeadSource/add_lead_source.html", context)

@login_required
def lead_source(request):

    lead_source_list = Lead_source.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Lead_source.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        lead_source = Lead_source.objects.create(name=name)
        lead_source.save()
    context = {"lead_source_list": lead_source_list}

    return render(request, "Admin/LeadSource/lead_source-list.html", context)


def check_lead_source(request):
    name = request.POST.get("name").capitalize()
    if Lead_source.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Lead Source already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Lead Source is available</div>"
        )


def edit_lead_source(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            lead_source = Lead_source.objects.get(id=id)
            lead_source.name = name
            lead_source.save()
            messages.success(request, "Lead Source updated successfully")
            return redirect("add_lead_source")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_lead_source")
    else:
        pass
    lead_source_list = Lead_source.objects.all()
    context = {
        "lead_source_list": lead_source_list,
        "message": "Lead Source Deleted Successfully!!!",
    }

    return render(request, "Admin/LeadSource/add_lead_source.html", context)


def delete_lead_source(request, id):
    lead_source = Lead_source.objects.get(id=id)
    lead_source.delete()
    messages.success(request, "Lead Source Deleted log for alertify!!!")
    return redirect("add_lead_source")

# ----------------------------- Banks ------------------------------------

@login_required
def add_bank(request):

    bank_list = Bank.objects.all()
    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()
    currency = Currency.objects.all()

    context = {
        "bank_list": bank_list,
        "message": "Bank Deleted Successfully!!!",
        "country": country,
        "state": state,
        "city": city,
        "currency": currency,
    }

    return render(request, "Admin/Bank/add_bank.html", context)

@login_required
def bank(request):

    bank_list = Bank.objects.all()
    if request.method == "POST":

        bank_name = request.POST.get("bank_name").capitalize()
        account_details = request.POST.get("account_details")
        countryid = request.POST.get("country_id")
        state_id = request.POST.get("state_id")
        city_id = request.POST.get("city_id")
        zip = request.POST.get("zip")
        address = request.POST.get("address")
        currency_id = request.POST.get("currency_id")

        country = Country.objects.get(id=countryid)
        currency = Currency.objects.get(id=currency_id)
        state = State.objects.get(id=state_id)
        city = City.objects.get(id=city_id)

        bank = Bank.objects.create(
            bank_name=bank_name,
            account_details=account_details,
            country=country,
            state=state,
            city=city,
            zip=zip,
            address=address,
            currency=currency,
        )
        bank.save()
    context = {"bank_list": bank_list}

    return render(request, "Admin/Bank/bank-list.html", context)


def get_states(request):
    country_id = request.GET.get("country_id")
    states = State.objects.filter(country_id=country_id).values_list("id", "name")
    return JsonResponse({"states": dict(states)})


def get_city(request):
    state_id = request.GET.get("state_id")
    citys = City.objects.filter(state_id=state_id).values_list("id", "name")
    return JsonResponse({"citys": dict(citys)})



def delete_bank(request, id):
    bank = Bank.objects.get(id=id)
    bank.delete()
    messages.success(request, "Bank Deleted log for alertify!!!")
    return redirect("add_bank")

# ----------------------------- Destination ------------------------------------

@login_required
def add_destination(request):

    destination_list = Destination.objects.all()
    country = Country.objects.all()

    context = {
        "destination_list": destination_list,
        "country": country,
        "message": "Destination Deleted Successfully!!!",
    }

    return render(request, "Admin/Destination/add_destination.html", context)


@login_required
def destination(request):

    destination_list = Destination.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        country_id = request.POST.get("country_id")

        country = Country.objects.get(id=country_id)

        if Destination.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        destination = Destination.objects.create(name=name, country=country)
        destination.save()
    context = {"destination_list": destination_list}

    return render(request, "Admin/Destination/destination-list.html", context)


def check_destination(request):
    name = request.POST.get("name").capitalize()
    if Destination.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Destination already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Destination is available</div>"
        )


def edit_destination(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            country_id = request.POST.get("country_id")

            country = Country.objects.get(id=country_id)

            destination = Destination.objects.get(id=id)
            destination.name = name
            destination.country = country
            destination.save()
            messages.success(request, "Destination updated successfully")
            return redirect("add_destination")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_destination")
    else:
        pass
    destination_list = Destination.objects.all()
    context = {
        "destination_list": destination_list,
        "message": "Destination Deleted Successfully!!!",
    }

    return render(request, "Admin/Destination/add_destination.html", context)


def delete_destination(request, id):
    destination = Destination.objects.get(id=id)
    destination.delete()
    messages.success(request, "Destination Deleted log for alertify!!!")
    return redirect("add_destination")

# ----------------------------- Restaurent Location ------------------------------------

@login_required
def add_restaurentlocation(request):

    restaurentlocation_list = Restaurent_location.objects.all()
    destination = Destination.objects.all()

    context = {
        "restaurentlocation_list": restaurentlocation_list,
        "destination": destination,
        "message": "Restaurent Location Deleted Successfully!!!",
    }

    return render(request, "Admin/RestaurentLocation/add_restaurent_location.html", context)


@login_required
def restaurentlocation(request):
    restaurentlocation_list = Restaurent_location.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        destination_id = request.POST.get("destination_id")

        destination = Destination.objects.get(id=destination_id)

        if Restaurent_location.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        restaurentlocation = Restaurent_location.objects.create(
            name=name, destination=destination
        )
        restaurentlocation.save()
    context = {"restaurentlocation_list": restaurentlocation_list}

    return render(request, "Admin/RestaurentLocation/restaurent_location-list.html", context)


def check_restaurentlocation(request):
    name = request.POST.get("name").capitalize()
    if Restaurent_location.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Restaurent Location already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Restaurent Location is available</div>"
        )


def edit_restaurentlocation(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            destination_id = request.POST.get("destination_id")

            destination = Destination.objects.get(id=destination_id)

            restaurentlocation = Restaurent_location.objects.get(id=id)
            restaurentlocation.name = name
            restaurentlocation.destination = destination
            restaurentlocation.save()
            messages.success(request, "Restaurent Location updated successfully")
            return redirect("add_restaurentlocation")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_restaurentlocation")
    else:
        pass
    restaurentlocation_list = Restaurent_location.objects.all()
    context = {
        "restaurentlocation_list": restaurentlocation_list,
        "message": "Restaurant Location Deleted Successfully!!!",
    }

    return render(request, "Admin/RestaurentLocation/add_restaurent_location.html", context)


def delete_restaurentlocation(request, id):
    restaurentlocation = Restaurent_location.objects.get(id=id)
    restaurentlocation.delete()
    messages.success(request, "Restaurant Location Deleted log for alertify!!!")
    return redirect("add_restaurentlocation")



# ----------------------------- Restaurent Type ------------------------------------

@login_required
def add_restaurenttype(request):

    restaurenttype_list = Restaurent_type.objects.all()

    context = {
        "restaurenttype_list": restaurenttype_list,
        "message": "Restaurent Type Deleted Successfully!!!",
    }

    return render(request, "Admin/RestaurentType/add_restaurent_type.html", context)


@login_required
def restaurenttype(request):
    restaurenttype_list = Restaurent_type.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Restaurent_type.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        restaurenttype = Restaurent_type.objects.create(name=name)
        restaurenttype.save()
    context = {"restaurenttype_list": restaurenttype_list}

    return render(request, "Admin/RestaurentType/restaurent_type-list.html", context)


def check_restaurenttype(request):
    name = request.POST.get("name").capitalize()
    if Restaurent_type.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Restaurent type already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Restaurent type is available</div>"
        )


def edit_restaurenttype(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()

            restaurenttype = Restaurent_type.objects.get(id=id)
            restaurenttype.name = name
            restaurenttype.save()
            messages.success(request, "Restaurent Type updated successfully")
            return redirect("add_restaurenttype")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_restaurenttype")
    else:
        pass
    restaurenttype_list = Restaurent_type.objects.all()
    context = {
        "restaurenttype_list": restaurenttype_list,
        "message": "Restaurant Type Deleted Successfully!!!",
    }

    return render(request, "Admin/RestaurentType/add_restaurent_type.html", context)


def delete_restaurenttype(request, id):
    restaurenttype = Restaurent_type.objects.get(id=id)
    restaurenttype.delete()
    messages.success(request, "Restaurant Type Deleted log for alertify!!!")
    return redirect("add_restaurenttype")


# ----------------------------- Special Days ------------------------------------

@login_required
def add_specialdays(request):

    specialdays_list = Special_days.objects.all()

    context = {
        "specialdays_list": specialdays_list,
        "message": "Special Days Deleted Successfully!!!",
    }

    return render(request, "Admin/SpecialDays/add_special_days.html", context)


@login_required
def specialdays(request):
    specialdays_list = Special_days.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        block_out_from_date = request.POST.get("block_out_from_date")
        block_out_to_date = request.POST.get("block_out_to_date")

        if Special_days.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        specialdays = Special_days.objects.create(
            name=name,
            block_out_from_date=block_out_from_date,
            block_out_to_date=block_out_to_date,
        )
        specialdays.save()
    context = {"specialdays_list": specialdays_list}

    return render(request, "Admin/SpecialDays/special_days-list.html", context)


def check_specialdays(request):
    name = request.POST.get("name").capitalize()
    if Special_days.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Special Days already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Special Days is available</div>"
        )


def edit_specialdays(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            block_out_from_date = request.POST.get("block_out_from_date")
            block_out_to_date = request.POST.get("block_out_to_date")

            specialdays = Special_days.objects.get(id=id)
            specialdays.name = name
            specialdays.block_out_from_date = block_out_from_date
            specialdays.block_out_to_date = block_out_to_date

            specialdays.save()
            messages.success(request, "Special Days updated successfully")
            return redirect("add_specialdays")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_specialdays")
    else:
        pass
    specialdays_list = Special_days.objects.all()
    context = {
        "specialdays_list": specialdays_list,
        "message": "Special Days Deleted Successfully!!!",
    }

    return render(request, "Admin/SpecialDays/add_special_days.html", context)


def delete_specialdays(request, id):
    specialdays = Special_days.objects.get(id=id)
    specialdays.delete()
    messages.success(request, "Special Days Deleted log for alertify!!!")
    return redirect("add_specialdays")


# ----------------------------- Room Type ------------------------------------

@login_required
def add_roomtype(request):

    roomtype_list = Room_type.objects.all()

    context = {
        "roomtype_list": roomtype_list,
        "message": "Room Type Deleted Successfully!!!",
    }

    return render(request, "Admin/RoomType/add_roomtype.html", context)


@login_required
def roomtype(request):

    roomtype_list = Room_type.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        remarks = request.POST.get("remarks")

        if Room_type.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        roomtype = Room_type.objects.create(name=name, remarks=remarks)
        roomtype.save()
    context = {"roomtype_list": roomtype_list}

    return render(request, "Admin/RoomType/roomtype-list.html", context)


def check_roomtype(request):
    name = request.POST.get("name").capitalize()
    if Room_type.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Room Type already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Room Type is available</div>"
        )


def edit_roomtype(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            remarks = request.POST.get("remarks")
            roomtype = Room_type.objects.get(id=id)
            roomtype.name = name
            roomtype.remarks = remarks
            roomtype.save()
            messages.success(request, "Room Type updated successfully")
            return redirect("add_roomtype")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_roomtype")
    else:
        pass
    roomtype_list = Room_type.objects.all()
    context = {
        "roomtype_list": roomtype_list,
        "message": "Room Type Deleted Successfully!!!",
    }

    return render(request, "Admin/Room Type/add_roomtype.html", context)



def delete_roomtype(request, id):
    roomtype = Room_type.objects.get(id=id)
    roomtype.delete()
    messages.success(request, "Room Type Deleted log for alertify!!!")
    return redirect("add_roomtype")


# ----------------------------- Hotel Location ------------------------------------

@login_required
def add_hotellocation(request):

    hotellocation_list = Hotel_location.objects.all()
    destination = Destination.objects.all()

    context = {
        "hotellocation_list": hotellocation_list,
        "destination": destination,
        "message": "Hotel Location Deleted Successfully!!!",
    }

    return render(request, "Admin/HotelLocation/add_hotel_location.html", context)


@login_required
def hotellocation(request):
    hotellocation_list = Hotel_location.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        destination_id = request.POST.get("destination_id")

        destination = Destination.objects.get(id=destination_id)

        if Hotel_location.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        hotellocation = Hotel_location.objects.create(
            name=name, destination=destination
        )
        hotellocation.save()
    context = {"hotellocation_list": hotellocation_list}

    return render(request, "Admin/HotelLocation/hotel_location-list.html", context)


def check_hotellocation(request):
    name = request.POST.get("name").capitalize()
    if Hotel_location.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Hotel Location already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Hotel Location is available</div>"
        )


def edit_hotellocation(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            destination_id = request.POST.get("destination_id")

            destination = Destination.objects.get(id=destination_id)

            hotellocation = Hotel_location.objects.get(id=id)
            hotellocation.name = name
            hotellocation.destination = destination
            hotellocation.save()
            messages.success(request, "Hotel Location updated successfully")
            return redirect("add_hotellocation")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_hotellocation")
    else:
        pass
    hotellocation_list = Hotel_location.objects.all()
    context = {
        "hotellocation_list": hotellocation_list,
        "message": "Hotel Location Deleted Successfully!!!",
    }

    return render(request, "Admin/HotelLocation/add_hotel_location.html", context)


def delete_hotellocation(request, id):
    hotellocation = Hotel_location.objects.get(id=id)
    hotellocation.delete()
    messages.success(request, "Hotel Location Deleted log for alertify!!!")
    hotellocation_list = Hotel_location.objects.all()
    context = {
        "hotellocation_list": hotellocation_list,
        "message": "Hotel Location Deleted Successfully!!!",
    }
    return render(request, "Admin/HotelLocation/hotel_location-list.html", context)



# ----------------------------- Visa ------------------------------------


@login_required
def add_visa(request):

    visa_list = Visa.objects.all()
    currency = Currency.objects.all()

    context = {
        "visa_list": visa_list,
        "message": "Visa Deleted Successfully!!!",
        "currency":currency
    }

    return render(request, "Admin/Visa/add_visa.html", context)


@login_required
def visa(request):

    visa_list = Visa.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        currency_id = request.POST.get("currency_id")
        adult_cost = request.POST.get("adult")
        child_cost = request.POST.get("child")
        infant_cost = request.POST.get("infant")
        currency = Currency.objects.get(id=currency_id)

        if Visa.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        visa = Visa.objects.create(
            name=name , currency=currency , adult_cost=adult_cost , child_cost=child_cost , infant_cost=infant_cost
        )
        visa.save()
    context = {"visa_list": visa_list}

    return render(request, "Admin/Visa/visa-list.html", context)


def check_visa(request):
    name = request.POST.get("name").capitalize()
    if Visa.objects.filter(name=name).exists():
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Visa already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Visa is available</div>"
        )


def edit_visa(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            currency_id = request.POST.get("currency_id")
            adult_cost = request.POST.get("adult_cost")
            child_cost = request.POST.get("child_cost")
            infant_cost = request.POST.get("infant_cost")
            currency = Currency.objects.get(id=currency_id)
            visa = Visa.objects.get(id=id)
            visa.name = name
            visa.adult_cost = adult_cost
            visa.child_cost = child_cost
            visa.infant_cost = infant_cost
            visa.currency = currency
            visa.save()
            messages.success(request, "Visa updated successfully")
            return redirect("add_visa")  
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_visa")  
    else:
        pass
    visa_list = Visa.objects.all()
    context = {
        "visa_list": visa_list,
        "message": "Visa Deleted Successfully!!!",
    }

    return render(request, "Admin/Visa/add_visa.html", context)


def delete_visa(request, id):
    visa = Visa.objects.get(id=id)
    visa.delete()
    messages.success(request, "Visa Deleted log for alertify!!!")
    return redirect("add_visa")



# ----------------------------- Transfer Location ------------------------------------


@login_required
def add_transfer_location(request):

    transfer_location_list = Transfer_location.objects.all()

    context = {
        "transfer_location_list": transfer_location_list,
        "message": "Transfer Location Deleted Successfully!!!",
    }

    return render(request, "Admin/TransferLocation/add_Transfer_location.html", context)


@login_required
def transfer_location(request):
    transfer_location_list = Transfer_location.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Transfer_location.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        transfer_location = Transfer_location.objects.create(
            name=name
        )
        transfer_location.save()
    context = {"transfer_location_list": transfer_location_list}

    return render(request, "Admin/TransferLocation/Transfer_location-list.html", context)


def check_transfer_location(request):
    name = request.POST.get("name").capitalize()
    if Transfer_location.objects.filter(name=name).exists():
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Transfer Location already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Transfer Location is available</div>"
        )


def edit_transfer_location(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
    
            transfer_location = Transfer_location.objects.get(id=id)
            transfer_location.name = name
            transfer_location.save()
            messages.success(request, "Transfer Location updated successfully")
            return redirect("add_transfer_location")  
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_transfer_location")  
    else:
        pass
    transfer_location_list = Transfer_location.objects.all()
    context = {
        "transfer_location_list": transfer_location_list,
        "message": "Transfer Location Deleted Successfully!!!",
    }

    return render(request, "Admin/TransferLocation/add_Transfer_location.html", context)


def delete_transfer_location(request, id):
    transfer_location = Transfer_location.objects.get(id=id)
    transfer_location.delete()
    messages.success(request, "Transfer Location Deleted log for alertify!!!")
    return redirect("add_transfer_location")


# ----------------------------- Restaurant ------------------------------------
@login_required
def restaurant(request):

    restaurant_list = Restaurent.objects.all()
    

    context = {
        "restaurant_list": restaurant_list,
        "message": "Restaurant Deleted Successfully!!!",
    }

    return render(request, "Admin/Restaurant/restaurant.html", context)


@login_required
def add_restaurant(request):
    restaurant_list = Restaurent.objects.all()
    restaurant_location = Restaurent_location.objects.all()
    destinations = Destination.objects.all()
    restaurant_type = Restaurent_type.objects.all()
    types = Extra_Meal_Price.objects.all()
    
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        image = request.FILES.get("image")
        timing = request.POST.get("timing")
        destination_id = request.POST.get("destination_id")
        restauration_location_id = request.POST.get("restauration_location_id")
        meal_prefrence = request.POST.get("meal_prefrence")
        landmark = request.POST.get("landmark")
        restaurent_type_ids = request.POST.getlist("restaurent_type_ids")
        type_id = request.POST.get("type_id")
        address = request.POST.get("address")
        contact_person = request.POST.get("contact_person")
        contact_person_phone = request.POST.get("contact_person_phone")
        contact_person_email = request.POST.get("contact_person_email")
        landline_no = request.POST.get("landline_no")
        restaurent_details = request.POST.get("restaurent_details")
        destination = Destination.objects.get(id=destination_id)
        restaurant_location = Restaurent_location.objects.get(id=restauration_location_id)
        type = Extra_Meal_Price.objects.get(id=type_id)

        if Restaurent.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        restaurant = Restaurent.objects.create(
            name=name , image=image , timing=timing , destination=destination , meal_prefrence=meal_prefrence , landmark=landmark ,
            type=type , address=address , contact_person=contact_person , contact_person_phone=contact_person_phone , contact_person_email=contact_person_email , 
            landline_no=landline_no , restaurent_details=restaurent_details , restaurant_location=restaurant_location
        )
        restaurant.restaurent_type.add(*restaurent_type_ids)
        restaurant.save()
        return redirect("restaurant")
    context = {"restaurant_list": restaurant_list,  "destinations": destinations ,"restaurant_location":restaurant_location , "restaurant_type":restaurant_type , "types":types}

    return render(request, "Admin/Restaurant/add_restaurant.html", context)


def get_restaurant_locations(request):
    destination_id = request.GET.get("destination_id")
    locations = list(Restaurent_location.objects.filter(destination_id=destination_id).values('id', 'name'))
    return JsonResponse(locations, safe=False)


def delete_restaurant(request, id):
    restaurant = Restaurent.objects.get(id=id)
    restaurant.delete()
    messages.success(request, "Restaurant Deleted log for alertify!!!")
    return redirect("restaurant")


def edit_restaurant(request, id):
    restaurant = get_object_or_404(Restaurent, id=id)
    restaurant_list = Restaurent.objects.all()
    restaurant_location = Restaurent_location.objects.all()
    destinations = Destination.objects.all()
    restaurant_type = Restaurent_type.objects.all()
    
   
    types = Extra_Meal_Price.objects.all()

    if request.method == "POST":
        name = request.POST.get("name").capitalize()
        image = request.FILES.get("image")
        timing = request.POST.get("timing")
        destination_id = request.POST.get("destination_id")
        restauration_location_id = request.POST.get("restauration_location_id")
        meal_prefrence = request.POST.get("meal_prefrence")
        landmark = request.POST.get("landmark")
        restaurent_type_ids = request.POST.getlist("restaurent_type_ids")
        type_id = request.POST.get("type_id")
        address = request.POST.get("address")
        contact_person = request.POST.get("contact_person")
        contact_person_phone = request.POST.get("contact_person_phone")
        contact_person_email = request.POST.get("contact_person_email")
        landline_no = request.POST.get("landline_no")
        restaurent_details = request.POST.get("restaurent_details")
        destination = Destination.objects.get(id=destination_id)
        restaurant_location = Restaurent_location.objects.get(id=restauration_location_id)
        type = Extra_Meal_Price.objects.get(id=type_id)

       
        restaurant.name = name
        if image:
            restaurant.image = image
        restaurant.timing = timing
        restaurant.destination = destination
        restaurant.meal_prefrence = meal_prefrence
        restaurant.landmark = landmark
        restaurant.type = type
        restaurant.address = address
        restaurant.contact_person = contact_person
        restaurant.contact_person_phone = contact_person_phone
        restaurant.contact_person_email = contact_person_email
        restaurant.landline_no = landline_no
        restaurant.restaurent_details = restaurent_details
        restaurant.restaurant_location = restaurant_location
        restaurant.restaurent_type.clear()
        restaurant.restaurent_type.add(*restaurent_type_ids)
        restaurant.save()

        return redirect("restaurant")

    context = {
        "restaurant": restaurant,
        "restaurant_list": restaurant_list,
        "destinations": destinations,
        "restaurant_location": restaurant_location,
        "restaurant_type": restaurant_type,
        "types": types,
       
    }

    return render(request, "Admin/Restaurant/edit_restaurant.html", context)

# ------------------------------ Guide -------------------------------------

@login_required
def add_guide(request):

    guide_list = Guide.objects.all()
    vechicle = Vehicle.objects.all()
    destination = Destination.objects.all()

    context = {
        "guide_list": guide_list,
        "message": "Guide Deleted Successfully!!!",
        "vechicle": vechicle,
        "destination":destination
    }

    return render(request, "Admin/Guide/add_guide.html", context)


@login_required
def guide(request):

    guide_list = Guide.objects.all()

    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        code = request.POST.get("code")
        mobile = request.POST.get("mobile")
        alternate_no = request.POST.get("alternate_no")
        id_passport = request.POST.get("id_passport")
        vehicle = request.POST.get("vehicle")
        address = request.POST.get("address")
        car_image = request.FILES.get("car_image")
        license_image = request.FILES.get("license_image")
        destination_covered_ids = request.POST.getlist("destination_covered_ids")
        language = request.POST.get("language")
        vehicle_id = Vehicle.objects.get(id=vehicle)

        # try:

        guide = Guide.objects.create(
            name=name,
            code=code,
            mobile=mobile,
            alternate_no=alternate_no,
            id_passport=id_passport,
            vehicle=vehicle_id,
            address=address,
            car_image=car_image,
            license_image=license_image,
            language=language
        )
        guide.destination_covered.add(*destination_covered_ids)

        guide.save()

        return HttpResponse("Guide created successfully!")

    context = {"guide_list": guide_list}

    return render(request, "Admin/Guide/guide-list.html", context)


# def edit_guide(request, id):
#     if request.method == "POST":
#         try:
#             name = request.POST.get("name").capitalize()
#             code = request.POST.get("code")
#             mobile = request.POST.get("mobile")
#             alternate_no = request.POST.get("alternate_no")
#             passport = request.POST.get("passport")
#             vehicle_id = request.POST.get("vehicle")
#             address = request.POST.get("address")
#             car_image = request.FILES.get("car_image")
#             licence_image = request.FILES.get("licence_image")

#             vehicle = Vehicle.objects.get(id=vehicle_id)
#             guide = guide.objects.get(id=id)
#             guide.name = name
#             guide.code = code
#             guide.mobile = mobile
#             guide.alternate_no = alternate_no
#             guide.passport = passport
#             guide.vehicle = vehicle
#             guide.address = address

#             if car_image:
#                 guide.car_image = car_image
#             if licence_image:
#                 guide.licence_image = licence_image

#             guide.save()
#             messages.success(request, "guide updated successfully")
#             return redirect("add_guide")
#         except Exception as e:
#             messages.error(request, f"Error occurred: {e}")
#             return redirect("add_guide")
#     else:
#         pass

#     return render(request, "Admin/guide/add_guide.html")


def delete_guide(request, id):
    guide = Guide.objects.get(id=id)
    guide.delete()
    messages.success(request, "Guide Deleted log for alertify!!!")
    return redirect("add_guide")


# ----------------------- Amenities -------------------


def checkamenities(request):
    ametinies_name = request.POST.get("ametinies_name").capitalize()

    if Amenities.objects.filter(name=ametinies_name).exists():

        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Amenities Name already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Amenities name is available</div>"
        )

@login_required
def amenities(request):

    amenities_list = Amenities.objects.all()

    context = {
        "amenities_list": amenities_list,
        "message": "Amenities Deleted Successfully!!!",
    }

    return render(request, "Admin/Amenities/amenities.html", context)


@login_required
def addamenities(request):

    if request.method == "POST":

        ammenities_name = request.POST.get("ametinies_name").capitalize()
        print("ssss", ammenities_name)

        if Amenities.objects.filter(name=ammenities_name).exists():

            message = "Amenities already exists"
            return HttpResponseBadRequest(message)

        ammenities = Amenities.objects.create(name=ammenities_name)
        ammenities.save()
        return redirect("amenities")


def editamenities(request, id):
    if request.method == "POST":
        try:
            ametinies_name = request.POST.get("ametinies_name").capitalize()
            amenities = Amenities.objects.get(id=id)
            amenities.name = ametinies_name
            amenities.save()
            messages.success(request, "Amenities updated successfully")
            return redirect("amenities")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("amenities")
    else:
        pass


def delete_amenities(request, id):
    amenities = Amenities.objects.get(id=id)
    amenities.delete()
    return redirect("amenities")


# ---------------------------- Arrivals -----------------------


def checkarrivals(request):
    arrivals_name = request.POST.get("arrivals_name").capitalize()

    if Arrival_Departure.objects.filter(name=arrivals_name).exists():

        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Arrival Name already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Arrival name is available</div>"
        )

@login_required
def arrivals(request):

    arrivals_list = Arrival_Departure.objects.all()

    context = {
        "arrivals_list": arrivals_list,
        "message": "Arrivals Deleted Successfully!!!",
    }

    return render(request, "Admin/ArrivalDeparture/arrival.html", context)


@login_required
def addarrivals(request):

    if request.method == "POST":

        arrivals_name = request.POST.get("arrivals_name").capitalize()

        if Arrival_Departure.objects.filter(name=arrivals_name).exists():

            message = "Arrivals already exists"
            return HttpResponseBadRequest(message)

        arrivals = Arrival_Departure.objects.create(name=arrivals_name)
        arrivals.save()
        return redirect("arrivals")


def editarrival(request, id):
    if request.method == "POST":
        try:
            arrivals_name = request.POST.get("arrivals_name").capitalize()

            arrival = Arrival_Departure.objects.get(id=id)
            arrival.name = arrivals_name
            arrival.save()
            messages.success(request, "Arrival Departure updated successfully")
            return redirect("arrivals")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("arrivals")
    else:
        pass


def delete_arrival(request, id):
    arrival = Arrival_Departure.objects.get(id=id)
    arrival.delete()
    return redirect("arrivals")



# ------------------------------ HOTEL -----------------------------------

@login_required
def hotel(request):

    hotel_list = Hotel.objects.all()
    

    context = {
        "hotel_list": hotel_list,
        "message": "Hotel Deleted Successfully!!!",
    }

    return render(request, "Admin/Hotel/hotel.html", context)

@login_required
def add_hotel(request):
    countrys = Country.objects.all()
    categorys = Hotel_Category.objects.all()
    amenitiess = Amenities.objects.all()
    roomtypes = Room_type.objects.all()
    mealplans = Meal_Plan.objects.all()
    destinations = Destination.objects.all()
    if request.method == "POST":
        name = request.POST.get("name").capitalize()
        country_id = request.POST.get("country_id")
        destination_id = request.POST.get("destination_id")
        category_id = request.POST.get("category_id")
        hotel_image = request.FILES.get("hotel_image")
        contact_person = request.POST.get("contact_person")
        tel_no = request.POST.get("tel_no")
        mob_no = request.POST.get("mob_no")
        reservation_email = request.POST.get("reservation_email")
        amenities_id = request.POST.getlist("amenities_id")
        hotel_contract = request.FILES.get("hotel_contract")
        room_type_id = request.POST.getlist("roomtype_id")
        meal_plan_id = request.POST.getlist("mealplan_id")
        hotel_address = request.POST.get("hotel_address")
        details = request.POST.get("details")
        supplier_own = request.POST.get("supplier_own") == 'on'
        country = Country.objects.get(id=country_id)
        destination = Destination.objects.get(id=destination_id)
        category = Hotel_Category.objects.get(id=category_id)
        
        hotel = Hotel.objects.create(name=name,country=country,destination=destination,category=category,hotel_image=hotel_image,
        contact_person=contact_person,tel_no=tel_no,mob_no=mob_no,reservation_email=reservation_email,hotel_contract=hotel_contract,
        hotel_address=hotel_address,details=details,supplier_own=supplier_own)
        hotel.amenities.add(*amenities_id)
        hotel.room_type.add(*room_type_id)
        hotel.meal_plan.add(*meal_plan_id)
        hotel.save()
        return redirect("hotel")
    context = {"countrys":countrys,"categorys":categorys,"amenitiess":amenitiess,"roomtypes":roomtypes,"mealplans":mealplans,"destinations":destinations}
    return render(request, "Admin/Hotel/addhotel.html",context)


def get_destination(request):
    country_id = request.GET.get("country_id")
    destinations = Destination.objects.filter(country_id=country_id).values_list("id", "name")
    return JsonResponse({"destinations": dict(destinations)})


def delete_hotel(request, id):
    hotel = Hotel.objects.get(id=id)
    hotel.delete()
    messages.success(request, "Hotel Deleted log for alertify!!!")
    return redirect("hotel")



# -------------------------------------- Extra Meal -------------------


def check_extrameal(request):
    extra_meal_name = request.POST.get("extra_meal_name").capitalize()

    if ExtraMeal.objects.filter(name=extra_meal_name).exists():
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Name already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>name is available</div>"
        )

@login_required
def extrameal(request):
    extra_meal = ExtraMeal.objects.all()
    context = {"extra_meal": extra_meal}
    return render(request, "Admin/ExtraMeal/extra_meal.html", context)

@login_required
def add_extrameal(request):
    destination = Destination.objects.all()
    location = Restaurent_location.objects.all()
    restaurant = Restaurent.objects.all()
    context = {
        "destination": destination,
        "location": location,
        "restaurant": restaurant,
    }
    if request.method == "POST":
        extra_meal_name = request.POST.get("extra_meal_name").capitalize()
        duration = request.POST.get("duration")
        restaurant_id = request.POST.get("restaurant_id")
        short_description = request.POST.get("short_description")
        description = request.POST.get("description")
        inclusion = request.POST.get("inclusion")
        useful_information = request.POST.get("useful_information")
        important_notes = request.POST.get("important_notes")

        restaurant = Restaurent.objects.get(id=restaurant_id)
        extra_meal = ExtraMeal.objects.create(
            name=extra_meal_name,
            meal_duration=duration,
            restaurant=restaurant,
            short_description=short_description,
            description=description,
            inclusions=inclusion,
            useful_information=useful_information,
            import_notes=important_notes,
        )
        extra_meal.save()
        return redirect("extrameal")

    return render(request, "Admin/ExtraMeal/add_extrameal.html", context)


def edit_extra_meal(request, id):

    destination = Destination.objects.all()
    location = Restaurent_location.objects.all()
    restaurant = Restaurent.objects.all()

    extra_meal = ExtraMeal.objects.get(id=id)

    if request.method == "POST":

        extra_meal_name = request.POST.get("extra_meal_name")

        duration = request.POST.get("duration")
        destination_id = request.POST.get("destination_id")
        restaurant_location_id = request.POST.get("restaurant_location_id")
        print("restaurant locatinn idddd::", restaurant_location_id)
        restaurant_id = request.POST.get("restaurant_id")
        short_description = request.POST.get("short_description")
        description = request.POST.get("description")
        inclusion = request.POST.get("inclusion")
        useful_information = request.POST.get("useful_information")
        important_notes = request.POST.get("important_notes")

        destnation = Destination.objects.get(id=destination_id)

        # restaurant_location = Restaurent_location.objects.get(id=restaurant_location_id)
        restaurant_location = Restaurent_location.objects.get(id=restaurant_location_id)
        restaurant = Restaurent.objects.get(id=restaurant_id)

        extra_meal.name = (extra_meal_name,)
        extra_meal.meal_duration = (duration,)
        extra_meal.restaurant_location = (restaurant_location,)
        extra_meal.restaurant = (restaurant,)
        extra_meal.short_description = (short_description,)
        extra_meal.description = (description,)
        extra_meal.inclusions = (inclusion,)
        extra_meal.useful_information = (useful_information,)
        extra_meal.import_notes = (important_notes,)

        extra_meal.save()
    context = {
        "destination": destination,
        "location": location,
        "restaurant": restaurant,
        "extra_meal": extra_meal,
    }
    return render(request, "Admin/ExtraMeal/edit_extrameal.html", context)


# ------------------------------- SightSeeing ----------------------------------------

@login_required
def add_sightseeing(request):

    destination = Destination.objects.all()
    days = Day.objects.all()
    context = {
        "destination": destination,
        "days": days,
    }
    if request.method == "POST":
        activity_name = request.POST.get("activity_name").capitalize()
        destination_id = request.POST.get("destination_id")
        activity_image = request.FILES.get("activity_image")
        tour_duration = request.POST.get("tour_duration")
        timings = request.POST.get("timings")
        operating_days_id = request.POST.getlist("operating_days_id")
        details = request.POST.get("details")
       
        destination = Destination.objects.get(id=destination_id)
        sightseeing = Sightseeing.objects.create(
            activity_name=activity_name,
            destination=destination,
            activity_image=activity_image,
            tour_duration=tour_duration,
            timings=timings,
            details=details,
        )
        sightseeing.operating_days.add(*operating_days_id)
        sightseeing.save()
        return redirect("sightseeing")

    return render(request, "Admin/Sightseeing/add_sightseeing.html", context)

@login_required
def sightseeing(request):
    sightseeing = Sightseeing.objects.all()
    context = {"sightseeing": sightseeing}
    return render(request, "Admin/Sightseeing/sightseeing.html", context)


def delete_sightseeing(request, id):

    sightseeing = Sightseeing.objects.get(id=id)
    sightseeing.delete()
    messages.success(request, "Sightseeing Deleted log for alertify!!!")
    return redirect("sightseeing")



# ------------------------------- Supplier ----------------------------------------

@login_required
def add_supplier(request):
    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()
    service_types = Service_type.objects.all()
    context = {
        "country": country,
        "state": state,
        "city": city,
        "service_types":service_types
    }
    if request.method == "POST":
        name = request.POST.get("name").capitalize()
        contact_person_name = request.POST.get("contact_person_name").capitalize()
        contact_person_designation = request.POST.get("contact_person_designation").capitalize()
        contact_person_email = request.POST.get("contact_person_email")
        landline_no = request.POST.get("landline_no")
        mob_no = request.POST.get("mob_no")
        service_type_id = request.POST.getlist("service_type_id")
        contract = request.FILES.get("contract")
        gst_vat = request.POST.get("gst_vat")
        countryid = request.POST.get("country_id")
        state_id = request.POST.get("state_id")
        city_id = request.POST.get("city_id")
        zip = request.POST.get("zip")
        address = request.POST.get("address")
       
        countrys = Country.objects.get(id=countryid)
        states = State.objects.get(id=state_id)
        citys= City.objects.get(id=city_id)
        supplier = Supplier.objects.create(
            name=name,
            contact_person_name=contact_person_name,
            contact_person_designation=contact_person_designation,
            contact_person_email=contact_person_email,
            landline_no=landline_no,
            mob_no=mob_no,
            contract=contract,
            gst_vat=gst_vat,
            zip=zip,
            address=address,
            country=countrys,
            state=states,
            city=citys,
            
        )
        supplier.service_type.add(*service_type_id)
        
        supplier.save()
        return redirect("supplier")

    return render(request, "Admin/Supplier/add_supplier.html", context)


@login_required
def supplier(request):
    supplier = Supplier.objects.all()
    context = {"supplier": supplier}
    return render(request, "Admin/Supplier/supplier.html", context)



def delete_supplier(request, id):
    supplier = Supplier.objects.get(id=id)
    supplier.delete()
    messages.success(request, "Supplier Deleted log for alertify!!!")
    return redirect("supplier")



# ------------------------------- Transfer ----------------------------------------


@login_required
def add_transfer(request):
    destination = Destination.objects.all()
    context = {
        "destination":destination
    }
    
    if request.method == "POST":
        transfer_name = request.POST.get("transfer_name").capitalize()
        transfer_type = request.POST.get("transfer_type")
        destination_id = request.POST.get("destination_id")
        transfer_images = request.FILES.get("transfer_images")
        tour_duration = request.POST.get("tour_duration")
        timings = request.POST.get("timings")
        description = request.POST.get("description")
       

        destination= Destination.objects.get(id=destination_id)
        transfer = Transfer.objects.create(
            transfer_name=transfer_name,
            transfer_type=transfer_type,
            destination=destination,
            transfer_images=transfer_images,
            tour_duration=tour_duration,
            timings=timings,
            description=description,
            
        )
        
        transfer.save()
        return redirect("transfer")

    return render(request, "Admin/Transfer/add_transfer.html", context)

@login_required
def transfer(request):
    transfer = Transfer.objects.all()
    context = {"transfer": transfer}
    return render(request, "Admin/Transfer/transfer.html", context)


def delete_transfer(request, id):
    transfer = Transfer.objects.get(id=id)
    transfer.delete()
    messages.success(request, "Transfer Deleted log for alertify!!!")
    return redirect("transfer")



# ------------------------------- Itinerary ----------------------------------------


@login_required
def add_itinerary(request):

    itinerary_list = Itinerary.objects.all()
    destinations = Destination.objects.all()
    transfers = Transfer.objects.all()
    sightseeings = Sightseeing.objects.all()

    context = {
        "itinerary_list": itinerary_list,
        "destinations":destinations,"transfers":transfers,"sightseeings":sightseeings,
        "message": "Special Days Deleted Successfully!!!",
    }

    return render(request, "Admin/Itinerary/add_itinerary.html", context)


@login_required
def itinerary(request):
    transfers_list = Transfer.objects.all()
    destinations = Destination.objects.all()
    transfers = Transfer.objects.all()
    sightseeings = Sightseeing.objects.all()
    if request.method == "POST":
            title = request.POST.get("title").capitalize()
            destination_id = request.POST.get("destination_id")
            previous_destination_id = request.POST.get("previous_destination_id")
            image = request.FILES.get("image")
            arrival_departure = request.POST.get("arrival_departure")
            transfer_ids = request.POST.getlist("transfer_ids")
            sightseeing_ids = request.POST.getlist("sightseeing_ids")
            description = request.POST.get("description")

            destination = Destination.objects.get(id=destination_id)
            previous_destination = Destination.objects.get(id=previous_destination_id)
            print(request.POST)

            itinerary = Itinerary.objects.create(
                title=title,
                destination=destination,
                previous_destination=previous_destination,
                image=image,
                arrival_departure=arrival_departure,
                description=description,
            )
            itinerary.transfer.add(*transfer_ids)
            itinerary.sightseeing.add(*sightseeing_ids)
            itinerary.save()
    context = {"transfers_list": transfers_list,
               "destinations":destinations,"transfers":transfers,"sightseeings":sightseeings}
    
    return render(request, "Admin/Itinerary/add_itinerary.html", context)


def delete_itinerary(request, id):
    itinerary = Itinerary.objects.get(id=id)
    itinerary.delete()
    messages.success(request, "Itinerary Deleted log for alertify!!!")
    return redirect("itinerary")


# ------------------------------- Documents ---------------------------

@login_required
def add_document(request):
    if request.method == "POST":
        folder_name = request.POST.get("folder_name")
        document_files = request.FILES.getlist("document_id")
        folder = Folder.objects.create(name=folder_name)
        for document_file in document_files:
            Document.objects.create(folder=folder, file=document_file)
        
        return HttpResponseRedirect(reverse('documents'))
        
    return render(request, "Admin/Documents/documents.html")


@login_required
def documents(request,):
    documents = Document.objects.all()
    context = {
        "documents": documents
    }
    return render(request, "Admin/Documents/documents.html", context)

def edit_document(request, id):
    document = Document.objects.get(id=id)
    
    # folder = get_object_or_404(Folder, id=id)
    if request.method == 'POST':
        documents = request.FILES.getlist("documents")  # Assuming you're expecting multiple files
        
        for doc in documents:
            document.document.add(doc)
        
        document.save()
        print("documents added:", documents)
    
        return HttpResponseRedirect(reverse('documents'))
    # print("heloooooooooooooooooooooo")
    # print("folder idddd",folder)
    # if request.method == 'POST':
    #     documents = request.FILES.getlist("documents")
    #     if documents:
    #         # If new documents are being uploaded, create new Document objects
    #         for document_file in documents:
    #             Document.objects.create(folder=folder, file=document_file)
    #         return HttpResponseRedirect(reverse('documents'))
    #     else:
           
    #         pass
    # else:
    #     pass

def delete_document(request, folder_id, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    messages.success(request, "Document deleted!")
    return redirect("folder_detail", id=folder_id)


# ----------------------------- Role ------------------------------------

@login_required
def add_role(request):

    role_list = Role_Permission.objects.all()

    context = {
        "role_list": role_list,
        "message": "Role Deleted Successfully!!!",
    }

    return render(request, "Admin/Role/add_role.html", context)

@login_required
def role(request):

    role_list = Role_Permission.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        remarks = request.POST.get("remarks")

        if Role_Permission.objects.filter(name=name):
            return HttpResponseBadRequest("WRONG")
        role = Role_Permission.objects.create(name=name,remarks=remarks)
        role.save()
    context = {"role_list": role_list}

    return render(request, "Admin/Role/role-list.html", context)


def check_role(request):
    name = request.POST.get("name").capitalize()
    if Role_Permission.objects.filter(name=name):
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Role already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Role is available</div>"
        )


def edit_role(request, id):
    if request.method == "POST":
        try:
            name = request.POST.get("name").capitalize()
            remarks = request.POST.get("remarks")
            role = Role_Permission.objects.get(id=id)
            role.name = name
            role.remarks = remarks
            role.save()
            messages.success(request, "Role updated successfully")
            return redirect("add_role")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect("add_role")
    else:
        pass
    role_list = Role_Permission.objects.all()
    context = {
        "role_list": role_list,
        "message": "Role Deleted Successfully!!!",
    }

    return render(request, "Admin/Role/add_role.html", context)


def delete_role(request, id):
    role = Role_Permission.objects.get(id=id)
    role.delete()
    messages.success(request, "Role Deleted log for alertify!!!")
    return redirect("add_role")



# ---------------------------------------- USER -------------------------------------


@login_required
def add_user(request):
    roles = Role_Permission.objects.all()
    reporting = CustomUser.objects.all()
    countrys = Country.objects.all()
    states = State.objects.all()
    citys = City.objects.all()
    destinations = Destination.objects.all()
    logged_in_user = request.user
    context = {
        'roles':roles,
        'reporting':reporting,
        'countrys':countrys,
        'states':states,
        'citys':citys,
        'destinations':destinations
    }
    if request.method == "POST":
        firstname = request.POST.get("firstname").capitalize()
        lastname = request.POST.get("lastname").capitalize()
        email = request.POST.get("email")
        code = request.POST.get("code")
        if not code:
            code = "+91"
        contact = request.POST.get("contact")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")
        destination_id = request.POST.get('destination_ids')
        reporting_to_id = request.POST.get("reporting_to_id")
        country_id = request.POST.get("country_id")
        state_id = request.POST.get("state_id")
        city_id = request.POST.get("city_id")
        pin = request.POST.get("pin")
        address = request.POST.get("address")
        reporting_to = CustomUser.objects.get(id=reporting_to_id)
        country = Country.objects.get(id=country_id)
        state = State.objects.get(id=state_id)
        city = City.objects.get(id=city_id)
        destination = Destination.objects.get(id=destination_id)
        user = CustomUser.objects.create_user(
            username=email,
            first_name=firstname,
            last_name=lastname,
            email=email,
            password=password,
            code=code,
            contact=contact,
            user_type = user_type,
            destination = destination
        )

        user.admin.reporting_to = reporting_to
        user.admin.country = country
        user.admin.state = state
        user.admin.city = city
        user.admin.pin = pin
        user.admin.address = address
        user.admin.registered_by = logged_in_user
        user.save()
        messages.success(
            request,
            f"{email} Created Successfully !!!",
        )
        return redirect("user")
    return render(request, "Admin/User/addadmin.html",context)


@login_required
def user(request):
    user = Admin.objects.all().order_by("-id")
    context = {
        "user":user
    }
    return render(request,"Admin/User/user.html",context)



# ------------------------------------ Query ---------------------------------------------
@login_required
def allquerylist(request):
    context = {} 
    
    if request.method == "GET":
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
    
    if request.user.is_authenticated:
        user_type = request.user.user_type  
        if user_type == "Admin":
            if from_date and to_date:
                all_lead = Lead.objects.filter(from_date__gte=from_date, to_date__lte=to_date)
            else:
                all_lead = Lead.objects.all().order_by("-id")
            new_lead_list = Lead.objects.filter(lead_status="Pending").order_by("-id")
            lead_list = Lead.objects.filter(lead_status="Connected").order_by("-id")
            quatation_lead_list = Lead.objects.filter(lead_status="Quotation Send").order_by("-id")
            paydonelead_list = Lead.objects.filter(Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")).order_by("-id")
            comlead_list = Lead.objects.filter(lead_status="Completed").order_by("-id")
            lost_list = Lead.objects.filter(lead_status="Lost").order_by("-id")
        elif user_type == "Sales Person":
            if from_date and to_date:
                all_lead = Lead.objects.filter(Q(added_by=request.user) | Q(sales_person=request.user)&
                    Q(from_date__gte=from_date, to_date__lte=to_date)).order_by("-id")
            else:
                all_lead = Lead.objects.filter(Q(added_by=request.user) | Q(sales_person=request.user)).order_by("-id")
            new_lead_list = Lead.objects.filter(Q(lead_status="Pending") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lead_list = Lead.objects.filter(Q(lead_status="Connected") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            quatation_lead_list = Lead.objects.filter(Q(lead_status="Quotation Send") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            paydonelead_list = Lead.objects.filter((Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")) & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            comlead_list = Lead.objects.filter(Q(lead_status="Completed") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lost_list = Lead.objects.filter(Q(lead_status="Lost") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
    else:
        
        new_lead_list = lead_list = quatation_lead_list = paydonelead_list = comlead_list = lost_list = all_lead = []


    operation = CustomUser.objects.filter(user_type="Sales Person")
    user = request.user
    authorizations = user.authorization
    # lead_authorization = Lead.objects.get(added_by__authorization=authorizations)
    recording_urls_and_dates = fetch_recording_urls_and_dates()

    context = {
        "new_lead_list": new_lead_list,
        "lead_list": lead_list,
        "quatation_lead_list": quatation_lead_list,
        "paydonelead_list": paydonelead_list,
        "comlead_list": comlead_list,
        "all_lead": all_lead,
        "lost_list": lost_list,
        "operation": operation,
        'recording_urls_and_dates': recording_urls_and_dates
    }
    return render(request,"Admin/Query/allquery.html",context)


@login_required
def newquerylist(request):
    context = {} 
    
    if request.method == "GET":
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        
    if request.user.is_authenticated:
        user_type = request.user.user_type  
        if user_type == "Admin":
            all_lead = Lead.objects.all().order_by("-id")
            if from_date and to_date:
                new_lead_list = Lead.objects.filter(lead_status="Pending", from_date__gte=from_date, to_date__lte=to_date).order_by("-id")
            else:
                new_lead_list = Lead.objects.filter(lead_status="Pending").order_by("-id")
            lead_list = Lead.objects.filter(lead_status="Connected").order_by("-id")
            quatation_lead_list = Lead.objects.filter(lead_status="Quotation Send").order_by("-id")
            paydonelead_list = Lead.objects.filter(Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")).order_by("-id")
            comlead_list = Lead.objects.filter(lead_status="Completed").order_by("-id")
            lost_list = Lead.objects.filter(lead_status="Lost").order_by("-id")
        elif user_type == "Sales Person":
            all_lead = Lead.objects.filter(Q(added_by=request.user) | Q(sales_person=request.user)).order_by("-id")
            if from_date and to_date:
                new_lead_list = Lead.objects.filter(
                    Q(lead_status="Pending") &
                    (Q(added_by=request.user) | Q(sales_person=request.user)) &
                    Q(from_date__gte=from_date, to_date__lte=to_date)
                ).order_by("-id")
            else:
                new_lead_list = Lead.objects.filter(Q(lead_status="Pending") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lead_list = Lead.objects.filter(Q(lead_status="Connected") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            quatation_lead_list = Lead.objects.filter(Q(lead_status="Quotation Send") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            paydonelead_list = Lead.objects.filter((Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")) & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            comlead_list = Lead.objects.filter(Q(lead_status="Completed") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lost_list = Lead.objects.filter(Q(lead_status="Lost") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
    else:
        
        new_lead_list = lead_list = quatation_lead_list = paydonelead_list = comlead_list = lost_list = all_lead = []

    operation = CustomUser.objects.filter(user_type="Sales Person")
    recording_urls_and_dates = fetch_recording_urls_and_dates()
    context = {
        "new_lead_list":new_lead_list,
        "lead_list":lead_list,
        "quatation_lead_list":quatation_lead_list,
        "paydonelead_list":paydonelead_list,
        "comlead_list":comlead_list,
        "all_lead":all_lead,
        "lost_list":lost_list,
        "operation":operation,
        "recording_urls_and_dates":recording_urls_and_dates

    }
    return render(request,"Admin/Query/newquery.html",context)

@login_required
def connectedquerylist(request):
    context = {} 
    
    if request.method == "GET":
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        
    if request.user.is_authenticated:
        user_type = request.user.user_type  
        if user_type == "Admin":
            all_lead = Lead.objects.all().order_by("-id")
            new_lead_list = Lead.objects.filter(lead_status="Pending").order_by("-id")
            if from_date and to_date:
                lead_list = Lead.objects.filter(lead_status="Connected",from_date__gte=from_date, to_date__lte=to_date).order_by("-id")
            else:
                lead_list = Lead.objects.filter(lead_status="Connected").order_by("-id")
            quatation_lead_list = Lead.objects.filter(lead_status="Quotation Send").order_by("-id")
            paydonelead_list = Lead.objects.filter(Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")).order_by("-id")
            comlead_list = Lead.objects.filter(lead_status="Completed").order_by("-id")
            lost_list = Lead.objects.filter(lead_status="Lost").order_by("-id")
        elif user_type == "Sales Person":
            all_lead = Lead.objects.filter(Q(added_by=request.user) | Q(sales_person=request.user)).order_by("-id")
            new_lead_list = Lead.objects.filter(Q(lead_status="Pending") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            if from_date and to_date:
                lead_list = Lead.objects.filter(Q(lead_status="Connected") & (Q(added_by=request.user) | Q(sales_person=request.user))&
                    Q(from_date__gte=from_date, to_date__lte=to_date)).order_by("-id")
            else:
                lead_list = Lead.objects.filter(Q(lead_status="Connected") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            quatation_lead_list = Lead.objects.filter(Q(lead_status="Quotation Send") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            paydonelead_list = Lead.objects.filter((Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")) & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            comlead_list = Lead.objects.filter(Q(lead_status="Completed") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lost_list = Lead.objects.filter(Q(lead_status="Lost") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
    else:
        
        new_lead_list = lead_list = quatation_lead_list = paydonelead_list = comlead_list = lost_list = all_lead = []

    operation = CustomUser.objects.filter(user_type="Sales Person")
    recording_urls_and_dates = fetch_recording_urls_and_dates()
    context = {
        "new_lead_list":new_lead_list,
        "lead_list":lead_list,
        "quatation_lead_list":quatation_lead_list,
        "paydonelead_list":paydonelead_list,
        "comlead_list":comlead_list,
        "all_lead":all_lead,
        "lost_list":lost_list,
        "operation":operation,
        "recording_urls_and_dates":recording_urls_and_dates
    }
    return render(request,"Admin/Query/connectedquery.html",context)

@login_required
def quatationquerylist(request):
    context = {} 
    
    if request.method == "GET":
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        
    if request.user.is_authenticated:
        user_type = request.user.user_type  
        if user_type == "Admin":
            all_lead = Lead.objects.all().order_by("-id")
            new_lead_list = Lead.objects.filter(lead_status="Pending").order_by("-id")
            lead_list = Lead.objects.filter(lead_status="Connected").order_by("-id")
            if from_date and to_date:
                quatation_lead_list = Lead.objects.filter(lead_status="Quotation Send",from_date__gte=from_date, to_date__lte=to_date).order_by("-id")
            else:
                quatation_lead_list = Lead.objects.filter(lead_status="Quotation Send").order_by("-id")
            paydonelead_list = Lead.objects.filter(Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")).order_by("-id")
            comlead_list = Lead.objects.filter(lead_status="Completed").order_by("-id")
            lost_list = Lead.objects.filter(lead_status="Lost").order_by("-id")
        elif user_type == "Sales Person":
            all_lead = Lead.objects.filter(Q(added_by=request.user) | Q(sales_person=request.user)).order_by("-id")
            new_lead_list = Lead.objects.filter(Q(lead_status="Pending") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lead_list = Lead.objects.filter(Q(lead_status="Connected") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            if from_date and to_date:
                quatation_lead_list = Lead.objects.filter(Q(lead_status="Quotation Send") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            else:
                quatation_lead_list = Lead.objects.filter(Q(lead_status="Quotation Send") & (Q(added_by=request.user) | Q(sales_person=request.user))&
                    Q(from_date__gte=from_date, to_date__lte=to_date)).order_by("-id")
            paydonelead_list = Lead.objects.filter((Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")) & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            comlead_list = Lead.objects.filter(Q(lead_status="Completed") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lost_list = Lead.objects.filter(Q(lead_status="Lost") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
    else:
        
        new_lead_list = lead_list = quatation_lead_list = paydonelead_list = comlead_list = lost_list = all_lead = []

    operation = CustomUser.objects.filter(user_type="Sales Person")
    recording_urls_and_dates = fetch_recording_urls_and_dates()
    context = {
        "new_lead_list":new_lead_list,
        "lead_list":lead_list,
        "quatation_lead_list":quatation_lead_list,
        "paydonelead_list":paydonelead_list,
        "comlead_list":comlead_list,
        "all_lead":all_lead,
        "lost_list":lost_list,
        "operation":operation,
        "recording_urls_and_dates":recording_urls_and_dates
    }
    return render(request,"Admin/Query/quatationquery-list.html",context)


@login_required
def paymentdonequerylist(request):
    url = "https://sandbox.cashfree.com/pg/links/testpoppee../orders"
    context = {} 
    
    if request.method == "GET":
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
    if request.user.is_authenticated:
        user_type = request.user.user_type  
        if user_type == "Admin":
            all_lead = Lead.objects.all().order_by("-id")
            new_lead_list = Lead.objects.filter(lead_status="Pending").order_by("-id")
            lead_list = Lead.objects.filter(lead_status="Connected").order_by("-id")
            quatation_lead_list = Lead.objects.filter(lead_status="Quotation Send").order_by("-id")
            if from_date and to_date:
                 paydonelead_list = Lead.objects.filter(
                    Q(lead_status="Payment Done") | Q(lead_status="Payment Processing"),
                    Q(from_date__gte=from_date, to_date__lte=to_date)
                ).order_by("-id")
            else:
                paydonelead_list = Lead.objects.filter(Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")).order_by("-id")
            comlead_list = Lead.objects.filter(lead_status="Completed").order_by("-id")
            lost_list = Lead.objects.filter(lead_status="Lost").order_by("-id")
        elif user_type == "Sales Person":
            all_lead = Lead.objects.filter(Q(added_by=request.user) | Q(sales_person=request.user)).order_by("-id")
            new_lead_list = Lead.objects.filter(Q(lead_status="Pending") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lead_list = Lead.objects.filter(Q(lead_status="Connected") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            quatation_lead_list = Lead.objects.filter(Q(lead_status="Quotation Send") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            if from_date and to_date:
                paydonelead_list = Lead.objects.filter(
                    (Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")) &
                    (Q(added_by=request.user) | Q(sales_person=request.user)),
                    Q(from_date__gte=from_date, to_date__lte=to_date)
                ).order_by("-id")
            else:
                paydonelead_list = Lead.objects.filter((Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")) & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            comlead_list = Lead.objects.filter(Q(lead_status="Completed") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lost_list = Lead.objects.filter(Q(lead_status="Lost") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
    else:
        
        new_lead_list = lead_list = quatation_lead_list = paydonelead_list = comlead_list = lost_list = all_lead = []

    operation = CustomUser.objects.filter(user_type="Sales Person")
    recording_urls_and_dates = fetch_recording_urls_and_dates()
    context = {
        "new_lead_list":new_lead_list,
        "lead_list":lead_list,
        "quatation_lead_list":quatation_lead_list,
        "operation":operation,
        "paydonelead_list":paydonelead_list,
        "comlead_list":comlead_list,
        "all_lead":all_lead,
        "lost_list":lost_list,
        "recording_urls_and_dates":recording_urls_and_dates
    }
    return render(request,"Admin/Query/paymentdonequery.html",context)


@login_required
def completedquerylist(request):
    context = {} 
    
    if request.method == "GET":
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
    if request.user.is_authenticated:
        user_type = request.user.user_type  
        if user_type == "Admin":
            all_lead = Lead.objects.all().order_by("-id")
            new_lead_list = Lead.objects.filter(lead_status="Pending").order_by("-id")
            lead_list = Lead.objects.filter(lead_status="Connected").order_by("-id")
            quatation_lead_list = Lead.objects.filter(lead_status="Quotation Send").order_by("-id")
            paydonelead_list = Lead.objects.filter(Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")).order_by("-id")
            if from_date and to_date:
                comlead_list = Lead.objects.filter(
                    lead_status="Completed",
                    from_date__gte=from_date,
                    to_date__lte=to_date
                ).order_by("-id")
            else:
                comlead_list = Lead.objects.filter(lead_status="Completed").order_by("-id")
            lost_list = Lead.objects.filter(lead_status="Lost").order_by("-id")
        elif user_type == "Sales Person":
            all_lead = Lead.objects.filter(Q(added_by=request.user) | Q(sales_person=request.user)).order_by("-id")
            new_lead_list = Lead.objects.filter(Q(lead_status="Pending") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lead_list = Lead.objects.filter(Q(lead_status="Connected") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            quatation_lead_list = Lead.objects.filter(Q(lead_status="Quotation Send") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            paydonelead_list = Lead.objects.filter((Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")) & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            if from_date and to_date:
                comlead_list = Lead.objects.filter(
                    Q(lead_status="Completed") &
                    (Q(added_by=request.user) | Q(sales_person=request.user)) &
                    Q(from_date__gte=from_date, to_date__lte=to_date)
                ).order_by("-id")
            else:
                comlead_list = Lead.objects.filter(Q(lead_status="Completed") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lost_list = Lead.objects.filter(Q(lead_status="Lost") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
    else:
        
        new_lead_list = lead_list = quatation_lead_list = paydonelead_list = comlead_list = lost_list = all_lead = []

    operation = CustomUser.objects.filter(user_type="Sales Person")
    recording_urls_and_dates = fetch_recording_urls_and_dates()
    context = {
        "new_lead_list":new_lead_list,
        "lead_list":lead_list,
        "quatation_lead_list":quatation_lead_list,
        "paydonelead_list":paydonelead_list,
        "comlead_list":comlead_list,
        "all_lead":all_lead,
        "lost_list":lost_list,
        "operation":operation,
        "recording_urls_and_dates":recording_urls_and_dates
    }
    return render(request,"Admin/Query/completedquery.html",context)


@login_required
def lostquerylist(request):
    context = {} 
    
    if request.method == "GET":
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
    if request.user.is_authenticated:
        user_type = request.user.user_type  
        if user_type == "Admin":
            all_lead = Lead.objects.all().order_by("-id")
            new_lead_list = Lead.objects.filter(lead_status="Pending").order_by("-id")
            lead_list = Lead.objects.filter(lead_status="Connected").order_by("-id")
            quatation_lead_list = Lead.objects.filter(lead_status="Quotation Send").order_by("-id")
            paydonelead_list = Lead.objects.filter(Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")).order_by("-id")
            comlead_list = Lead.objects.filter(lead_status="Completed").order_by("-id")
            if from_date and to_date:
                lost_list = Lead.objects.filter(lead_status="Lost",
                    from_date__gte=from_date,
                    to_date__lte=to_date).order_by("-id")
            else:
                lost_list = Lead.objects.filter(lead_status="Lost").order_by("-id")
        elif user_type == "Sales Person":
            all_lead = Lead.objects.filter(Q(added_by=request.user) | Q(sales_person=request.user)).order_by("-id")
            new_lead_list = Lead.objects.filter(Q(lead_status="Pending") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            lead_list = Lead.objects.filter(Q(lead_status="Connected") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            quatation_lead_list = Lead.objects.filter(Q(lead_status="Quotation Send") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            paydonelead_list = Lead.objects.filter((Q(lead_status="Payment Done") | Q(lead_status="Payment Processing")) & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            comlead_list = Lead.objects.filter(Q(lead_status="Completed") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
            if from_date and to_date:
                lost_list = Lead.objects.filter(
                    Q(lead_status="Lost") &
                    (Q(added_by=request.user) | Q(sales_person=request.user)) &
                    Q(from_date__gte=from_date, to_date__lte=to_date)
                ).order_by("-id")
            else:
                lost_list = Lead.objects.filter(Q(lead_status="Lost") & (Q(added_by=request.user) | Q(sales_person=request.user))).order_by("-id")
    else:
        
        new_lead_list = lead_list = quatation_lead_list = paydonelead_list = comlead_list = lost_list = all_lead = []

    operation = CustomUser.objects.filter(user_type="Sales Person")
    recording_urls_and_dates = fetch_recording_urls_and_dates()
    context = {
        "new_lead_list":new_lead_list,
        "lead_list":lead_list,
        "quatation_lead_list":quatation_lead_list,
        "operation":operation,
        "paydonelead_list":paydonelead_list,
        "comlead_list":comlead_list,
        "all_lead":all_lead,
        "lost_list":lost_list,
        "recording_urls_and_dates":recording_urls_and_dates,
    }
    return render(request,"Admin/Query/lostleads.html",context)

def getoperationdep():
    print(CustomUser.objects.filter(user_type = "Operation Person"))
    return CustomUser.objects.filter(user_type = "Operation Person")

       
@login_required
def addquery(request):
    servicess = Service_type.objects.all()
    destinations = Destination.objects.all()
    lead_sources = Lead_source.objects.all()
    operation = CustomUser.objects.filter(user_type = "Operation Person")
    sales = CustomUser.objects.filter(user_type = "Sales Person")
    context = {
        "servicess":servicess,
        "destinations":destinations,
        "lead_sources":lead_sources,
        "operation":operation,
        "sales":sales,
    }
    if request.method == "POST":
        contact_person_name = request.POST.get("contact_person_name").capitalize()
        contact_person_email = request.POST.get("contact_person_email")
        mobile_number = request.POST.get("mobile_number")
        if mobile_number and not mobile_number.startswith('+91'):
            mobile_number = '+91' + mobile_number
        alternate_mobile_number = request.POST.get("alternate_mobile_number")
        if alternate_mobile_number and not alternate_mobile_number.startswith('+91'):
            alternate_mobile_number = '+91' + alternate_mobile_number
        inter_domes = request.POST.get("inter_domes")
        destination_name = request.POST.get('destination_id')
        from_date = request.POST.get('from')
        to_date = request.POST.get('to')
        purpose_of_travel = request.POST.get('purpose_of_travel')
        service_type_id = request.POST.get("service_type_id")
        query_title = request.POST.get("query_title")
        budget = request.POST.get("budget")
        adult = request.POST.get("adult")
        child = request.POST.get("child")
        infants = request.POST.get("infants")
        lead_source_id = request.POST.get("lead_source_id")
        sales_person_id = request.POST.get("sales_person_id")
        other_information = request.POST.get("other_information")
        service_type = Service_type.objects.get(id=service_type_id)
        lead_source = Lead_source.objects.get(id=lead_source_id)
        sales_person = CustomUser.objects.get(id=sales_person_id)
        destination = Destination.objects.get(id=destination_name)
        
        
        lead = Lead.objects.create(
            name=contact_person_name,
            email=contact_person_email,
            mobile_number=mobile_number,
            alternate_mobile_number=alternate_mobile_number,
            inter_domes=inter_domes,
            destinations=destination,
            from_date=from_date,
            to_date=to_date,
            purpose_of_travel=purpose_of_travel,
            service_type=service_type,
            query_title=query_title,
            budget=budget,
            adult=adult,
            child=child,
            infants=infants,
            lead_source=lead_source,
            other_information=other_information,
            sales_person=sales_person)
        operation_persons=CustomUser.objects.filter(user_type = "Operation Person",destination=destination_name)

        if operation_persons.exists():
            last_assigned_index = cache.get("last_assigned_index") or 0
            next_index = (last_assigned_index + 1) % operation_persons.count()
            operation_person = operation_persons[next_index]
            lead.operation_person = operation_person
            cache.set("last_assigned_index", next_index)
        lead.lead_status = "Pending"
        lead.added_by = request.user
        lead.save()
        return redirect("allquerylist")
        

    return render(request,"Admin/Query/add-query.html",context)

@login_required
def editquery(request,id):
    servicess = Service_type.objects.all()
    destinations = Destination.objects.all()
    lead_sources = Lead_source.objects.all()
    operation = CustomUser.objects.filter(user_type = "Operation Person")
    sales = CustomUser.objects.filter(user_type = "Sales Person")
    lead = get_object_or_404(Lead, id=id)
    context = {
        "servicess":servicess,
        "destinations":destinations,
        "lead_sources":lead_sources,
        "operation":operation,
        "sales":sales,
        "query":lead,
    }
    
    if request.method == "POST":
        try:
            contact_person_name = request.POST.get("contact_person_name").capitalize()
            contact_person_email = request.POST.get("contact_person_email")
            mobile_number = request.POST.get("mobile_number")
            if mobile_number and not mobile_number.startswith('+91'):
                mobile_number = '+91' + mobile_number
            alternate_mobile_number = request.POST.get("alternate_mobile_number")
            if alternate_mobile_number and not alternate_mobile_number.startswith('+91'):
                alternate_mobile_number = '+91' + alternate_mobile_number
            inter_domes = request.POST.get("inter_domes")
            destination_name = request.POST.get('destination_id')
            from_date = request.POST.get('from')
            to_date = request.POST.get('to')
            purpose_of_travel = request.POST.get('purpose_of_travel')
            service_type_id = request.POST.get("service_type_id")
            query_title = request.POST.get("query_title")
            budget = request.POST.get("budget")
            adult = request.POST.get("adult")
            child = request.POST.get("child")
            infants = request.POST.get("infants")
            lead_source_id = request.POST.get("lead_source_id")
            sales_person_id = request.POST.get("sales_person_id")
            operation_person_id = request.POST.get("operation_person_id")
            other_information = request.POST.get("other_information")
            service_type = Service_type.objects.get(id=service_type_id)
            lead_source = Lead_source.objects.get(id=lead_source_id)
            sales_person = CustomUser.objects.get(id=sales_person_id)
            operation_person = CustomUser.objects.get(id=operation_person_id)
            destination = Destination.objects.get(id=destination_name)
 
            lead.name=contact_person_name
            lead.email=contact_person_email
            lead.inter_domes=inter_domes
            lead.mobile_number=mobile_number
            lead.alternate_mobile_number=alternate_mobile_number
            lead.destinations=destination
            lead.from_date=from_date
            lead.to_date=to_date
            lead.purpose_of_travel=purpose_of_travel
            lead.service_type=service_type
            lead.query_title=query_title
            lead.adult=adult
            lead.child=child
            lead.infants=infants
            lead.budget=budget
            lead.other_information=other_information
            lead.lead_source=lead_source
            lead.sales_person=sales_person
            lead.operation_person=operation_person
            lead.save()
            messages.success(request, "Query updated successfully")
            return redirect("allquerylist")
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
        return redirect("allquerylist")
    else:
        pass
    

    return render(request, "Admin/Query/edit_query.html",context)


def lead_status_update(request,id):
    lead = Lead.objects.get(id=id)
    if request.method == "POST":
        lead_status = request.POST.get("lead_status")
        lead.lead_status = lead_status
        lead.save()
        return redirect("allquerylist")
    

def op_update(request,id):
    lead = Lead.objects.get(id=id)
    if request.method == "POST":
        operation = request.POST.get("sales_person_id")
        sales_person = CustomUser.objects.get(id=operation)
        lead.sales_person = sales_person
        lead.save()
        return redirect("allquerylist")
    
    
def attach_quotation(request, id):
    if request.method == "POST":
        enq = request.POST.get("enq_id")
        attachments = request.FILES.getlist("attachment")
        
        try:
            lead = get_object_or_404(Lead, id=enq)
            quotation = Quatation.objects.create(lead=lead)
            
            for attachment in attachments:
                attachment_obj = Attachment.objects.create(file=attachment)
                quotation.attachment.add(attachment_obj)  

            lead.lead_status = "Quotation Send"  
            lead.save()
            activity_history = ActivityHistory.objects.create(lead=lead, activity_type='Quotation')

            quotation.activity = activity_history
            quotation.save()
            

            messages.success(request, "Quotation Added Successfully...")
            subject = "Travel Packages Quotation Attached"
            message = "Dear {},\n\nI hope this email finds you well. Find your dream vacation inside!  We've attached a detailed quotation outlining each package, including destinations, activities, pricing, and more. \nWe look forward to helping you plan your next adventure!".format(lead.name)
            email_from = settings.EMAIL_HOST_USER
            to_email = lead.email

            email = EmailMessage(subject, message, email_from, [to_email])
            
            for attachment in quotation.attachment.all():
                content_type, _ = mimetypes.guess_type(attachment.file.name)
                if content_type is None:
                    content_type = 'application/octet-stream' 
                email.attach(attachment.file.name, attachment.file.read(), content_type)
            
            email.send()
            
            media_attachments = []
            for attachment in quotation.attachment.all():
                attachment_url = request.build_absolute_uri(attachment.file.url)
                media_attachments.append({
                    "mediaUrl": attachment_url,
                    "mediaType": "image"  
                })
                

            aisensy_api_url = "https://backend.aisensy.com/campaign/t1/api/v2"
            api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1Zjk4M2ZmZTMxNWI1NDVjZDQ1Nzk3ZSIsIm5hbWUiOiJ0aGVza3l0cmFpbCA4NDEzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY1Zjk4M2ZmZTMxNWI1NDVjZDQ1Nzk3NCIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzEwODUxMDcxfQ.XnS_3uclP8c0J6drYjBCAQmbE6bHxGuD2IAGPaS4N9Y"

            payload = {
                "apiKey": api_key,
                "campaignName": "qq",
                "destination": lead.mobile_number, 
                "userName": "theskytrail 8413",
                "templateParams": [],
                "source": "new-landing-page form",
                "media": {
                    "attachments": media_attachments
                },
                "buttons": [],
                "carouselCards": [],
                "location": {}
            }

            response = requests.post(aisensy_api_url, json=payload)
            if response.status_code == 200:
                print("WhatsApp message sent successfully!")
            else:
                print("Failed to send WhatsApp message:", response.text)
            
        except Lead.DoesNotExist:
            pass
        
        return redirect("allquerylist")
    else:
        pass


def add_notes(request, id):
    if request.method == "POST":
        enq = request.POST.get("enq_id")
        notes = request.POST.get("notes")
        
        try:
            lead = get_object_or_404(Lead, id=enq)
            note = Notes.objects.create(lead=lead,notes=notes)
            activity_history = ActivityHistory.objects.create(lead=lead, activity_type='Note')
            note.activity = activity_history
            note.save()


            messages.success(request, "Note Added Successfully...")
        except Lead.DoesNotExist:
            pass
        
        return redirect("allquerylist")
    else:
        pass
    
    
def attach_confirmattachmnet(request, id):
    if request.method == "POST":
        enq = request.POST.get("enq_id")
        attachments = request.FILES.getlist("attachment")
        
        try:
            lead = get_object_or_404(Lead, id=enq)
            attach = ConfirmAttachment.objects.create(lead=lead)
            
            for attachment in attachments:
                attachment_obj = File.objects.create(file=attachment)
                attach.attachment.add(attachment_obj)  

            lead.save()
            activity_history = ActivityHistory.objects.create(lead=lead, activity_type='Attachment')

            attach.activity = activity_history
            attach.save()
            

            messages.success(request, "Attachment Added Successfully...")
            
        except Lead.DoesNotExist:
            pass
        
        return redirect("allquerylist")
    else:
        pass


def payment_link(request,id): 
    if request.method == "POST":
        
        email = request.POST.get("email")
        amount = request.POST.get("amount")
        lead = Lead.objects.get(id=id)
        
        # url = "https://api.cashfree.com/pg/orders"
        url = "https://sandbox.cashfree.com/pg/links"
                
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-version": "2023-08-01",
            "x-client-id": "17792263f8ad3b41a90673b52f229771",
            "x-client-secret": "00f09ad3074140b18466ebbb092f8e6066917028"
        }

        unique_link_id = str(uuid.uuid4())    
        print("uniquer:",unique_link_id)  
        data = {
            "customer_details": {
                "customer_phone": lead.mobile_number,
                "customer_email": email,
                "customer_name": lead.name
            },
            "link_notify": {
                "send_sms": True,
                "send_email": True
            },
            "link_amount": amount,
            "link_currency": "INR",
            "link_purpose": "Payment for PlayStation 11",
            "link_id": unique_link_id,
            "returnUrl":"http://127.0.0.1:8000/quatationquerylist",
            
        }


        response = requests.post(url, headers=headers, json=data)
        data = response.json()
        print("data response......",response.text)
        link_url = response.json().get('link_url')
        link_expiry_time = response.json().get('link_expiry_time')
        
        lead.lead_status="Payment Processing"
        lead.save()
        payment = Payment.objects.create(leads=lead,link_id=unique_link_id,payment_link=link_url,link_expiry_time=link_expiry_time)
        activity_history = ActivityHistory.objects.create(lead=lead, activity_type='Payment')
        payment.activity = activity_history
        payment.save()
        messages.success(request, "Payment Link Generated Successfully...")
        return redirect("quatationquerylist")


def payment_status(request,id):
    payment = Payment.objects.get(id=id)
    link_id=payment.link_id
   
    url = f"https://sandbox.cashfree.com/pg/links/{link_id}"
    headers = {
    "accept": "application/json",
    "x-api-version": "2023-08-01",
    "x-client-id": "17792263f8ad3b41a90673b52f229771",
    "x-client-secret": "00f09ad3074140b18466ebbb092f8e6066917028"
    }
    
    response = requests.get(url, headers=headers)   
    print("status show",response.text)
    data = response.json() 
    return JsonResponse(data)
  

def add_followup(request, id):
    if request.method == "POST":
        enq = request.POST.get("enq_id")
        note = request.POST.get("note")
        datetime = request.POST.get("datetime")
        
        try:
            lead = get_object_or_404(Lead, id=enq)
            followup = Followup.objects.create(lead=lead,note=note,datetime=datetime)
            
            activity_history = ActivityHistory.objects.create(lead=lead, activity_type='Followup')
            followup.activity = activity_history
            followup.save()

            messages.success(request, "Followup Added Successfully...")
        except Lead.DoesNotExist:
            pass
        
        return redirect("allquerylist")
    else:
        pass
    
    
def make_click_to_call(request,id):
   
    user = request.user
    print("hellooooooooo")
   
    lead = Lead.objects.get(id=id)
    print("lead mobile:",lead.mobile_number)
    url = "https://api-smartflo.tatateleservices.com/v1/click_to_call"

    # Define your payload and headers
    payload = {"agent_number": "0503637080052", "destination_number": lead.mobile_number}
    headers = {
        "accept": "application/json",
        "Authorization": lead.added_by.authorization,
        # "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzNjM3MDgiLCJpc3MiOiJodHRwczovL2Nsb3VkcGhvbmUudGF0YXRlbGVzZXJ2aWNlcy5jb20vdG9rZW4vZ2VuZXJhdGUiLCJpYXQiOjE3MDIyNzE2NzAsImV4cCI6MjAwMjI3MTY3MCwibmJmIjoxNzAyMjcxNjcwLCJqdGkiOiJCa0xPV05hcVNNVkZabm4wIn0.w76qiqkkFZpcb9sjIg_J9MG__iw7m0yZ-rlAoOGKab4",
        "content-type": "application/json",
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)
    json_text = response.text
    data_dict = json.loads(json_text)
    # print(type(data_dict)) 
    # print(data_dict['success'])

    # student_details = json.loads(jsonString)
    if data_dict['success'] == True:
       
        response_data = {"status": "calling"}

        return JsonResponse(response_data)

   
    else:
        
        response_data = {"error": "Failed to initiate call"}
        return JsonResponse(response_data, status=response.status_code)


@login_required
def profile(request):
    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()
    context = {
        'country':country,
        'state':state,
        'city':city,

        }
    return render(request,"Profile/user-profile.html",context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        country_id = request.POST.get('country')
        state_id = request.POST.get('state')
        address = request.POST.get('address')
        city_id = request.POST.get('city')
        pincode = request.POST.get('pincode')

        country = Country.objects.get(id=country_id)
        state = State.objects.get(id=state_id)
        city = City.objects.get(name=city_id)

        user = request.user
        user.username = username
        user.admin.country = country
        user.admin.state = state
        user.admin.city = city
        user.admin.address = address
        user.admin.pin = pincode
        user.save()
        
        return JsonResponse({'message': 'Profile update successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)




def userlogout (request):
    logout(request)
    return redirect("/")


def forgot_psw(request):
   
    if request.method == "POST":
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email):
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            email_template = render_to_string('password_reset_email.html', {
                'reset_link': reset_link,
            })
            email_subject = 'Reset your password'
            email_to = [email]
            email = EmailMessage(email_subject, email_template, to=email_to)
            email.send()
            return render(request, 'forgot_psw_success.html')
            
        else:
            messages.error(request,"email not found")
    return render(request,"forgot_psw.html")

def resetpsw(request):
    return render(request,"forgot_psw.html")

def forgot_psw_success(request):
    return render(request,'forgot_psw.html')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_change_form.html'  


def change_psw(request):
    user = request.user
    admin = Admin.objects.get(users=user)

    if request.method == "POST":
        old_psw = request.POST.get("old_password")
        newpassword = request.POST.get("newpassword")
        confirmpassword = request.POST.get("confirmpassword")

        if check_password(old_psw, admin.users.password):
            if newpassword == confirmpassword:
                admin.users.set_password(newpassword)
                admin.users.save()
                messages.success(
                    request, "Password changed successfully Please Login Again !!"
                )
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.success(request, "New passwords do not match")
                return HttpResponseRedirect(reverse("change_psw"))

        else:
            messages.warning(request, "Current password is not correct")
            return HttpResponseRedirect(reverse("change_psw"))

    return render(request, "AccountSetting/changepsw.html")




def testt(request,id):
    lead = Lead.objects.get(id=id)
    # print("heloooo")
    destination = lead.mobile_number
    # recording_urls_and_dates = fetch_recording_urls_and_dates()
    recording_urls_and_dates = LeadWiseCallRecords(destination)
    response_data = {"status": "calling","recording_urls_and_dates":recording_urls_and_dates}

    # response_data = {"recording_urls_and_dates": recording_urls_and_dates}
    # print("response data.....")


    return JsonResponse(response_data)

def demo(request):
    return render(request,"demo.html")


import pandas as pd

def bulk_lead_upload(request):
    if request.method == "POST":
        file = request.FILES.get("excel_file")
        if not file:
            messages.error(request, "No file uploaded.")
            return redirect("allquerylist")
            

        try:
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                
                
                name = row["name"].capitalize()
                email = row["email"]
                mobile_number = row["mobile_number"]
                if mobile_number:
                    if not str(mobile_number).startswith('+91'):
                        mobile_number = '+91' + str(mobile_number)
                inter_domes = row["inter_domes"]
                destination_name = row["destinations"]
                destination = Destination.objects.get(name=destination_name)
                from_date = row["from_date"]
                to_date = row["to_date"]
                purpose_of_travel = row["purpose_of_travel"]
                service_type_name = row["service_type"]
                service = Service_type.objects.get(name=service_type_name)
                query_title = row["query_title"]
                budget = row["budget"]
                adult = row["adult"]
                child = row["child"]
                infants = row["infants"]
                lead_source_name = row["lead_source"]
                lead_sources = Lead_source.objects.get(name=lead_source_name)
                other_information = row["other_information"]
              
                lead, created = Lead.objects.get_or_create(
                    name=name,
                    email=email,
                    mobile_number=mobile_number,
                    inter_domes=inter_domes,
                    destinations=destination,
                    from_date=from_date,
                    to_date=to_date,
                    purpose_of_travel=purpose_of_travel,
                    service_type=service,
                    query_title=query_title,
                    budget=budget,
                    adult=adult,
                    child=child,
                    infants=infants,
                    lead_source=lead_sources,
                    other_information=other_information,
                    lead_status="Pending",
                    added_by=request.user
                )
                
                if created:
                    lead.save()

            messages.success(request, "Data Imported Successfully!!")

        except Exception as e:
            print(f"Error occurred in iteration {index}: {str(e)}")
            
    return redirect("newquerylist")




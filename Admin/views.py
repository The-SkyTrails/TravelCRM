from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import *
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.
# from django.htmx import HtmxMixin
from django.views.generic import ListView


def dashboard(request):
    return render(request, "Admin/Dashboard/dashboard.html")


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

        if Country.objects.filter(country_name=country_name).exists():
            print("wrongggg")
            return HttpResponseBadRequest("WRONG")
        country = Country.objects.create(
            country_name=country_name, sort_name=sort_name, nationality=nationality
        )
        country.save()
        print("country nammeeee")
    context = {"country_list": country_list}

    return render(request, "Admin/Country/country-list.html", context)


def check_country(request):
    country_name = request.POST.get("country_name").capitalize()
    print("heloooo", country_name)
    if Country.objects.filter(country_name=country_name).exists():
        print("workinggggg")
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>Country Name already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>Country name is available</div>"
        )


def edit_Country(request, id):

    country_name = request.POST.get("country_name").capitalize()
    nationality = request.POST.get("nationality").capitalize()
    sort_name = request.POST.get("sort_name").capitalize()
    country = Country.objects.get(id=id)
    country.country_name = country_name
    country.nationality = nationality
    country.sort_name = sort_name
    country.save()
    country_list = Country.objects.all()
    context = {
        "country_list": country_list,
        "message": "Country Deleted Successfully!!!",
    }

    return render(request, "Admin/Country/add_country.html", context)
    # return JsonResponse({"success": True})


def delete_country(request, id):
    con = Country.objects.get(id=id)
    con.delete()
    messages.success(request, "Country Deleted log for alertify!!!")
    country_list = Country.objects.all()
    context = {
        "country_list": country_list,
        "message": "Country Deleted Successfully!!!",
    }
    return render(request, "Admin/Country/country-list.html", context)


# ---------------------------------


def checkstate(request):
    state_name = request.POST.get("state_name").capitalize()
    if State.objects.filter(name=state_name).exists():
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>State Name already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>State name is available</div>"
        )


def state(request):

    state_list = State.objects.all()
    country = Country.objects.all()

    context = {
        "state_list": state_list,
        "message": "State Deleted Successfully!!!",
        "country": country,
    }

    return render(request, "Admin/State/state.html", context)


def addstate(request):

    state_list = State.objects.all()
    if request.method == "POST":

        state_name = request.POST.get("state_name").capitalize()
        countryid = request.POST.get("country_id").capitalize()

        if State.objects.filter(name=state_name).exists():
            print("wrongggg")
            message = "State already exists"
            return HttpResponseBadRequest(message)
        country = Country.objects.get(id=countryid)
        state = State.objects.create(name=state_name, country=country)
        state.save()
        print("country nammeeee")
    context = {"state_list": state_list}

    return render(request, "Admin/State/state.html", context)


def editstate(request, id):

    state_name = request.POST.get("state_name").capitalize()
    country_id = request.POST.get("country_id").capitalize()

    country = Country.objects.get(id=country_id)
    state = State.objects.get(id=id)
    state.country = country
    state.name = state_name
    state.save()
    state_list = State.objects.all()
    context = {
        "state_list": state_list,
    }

    return redirect("state")

    # return render(request, "Admin/State/state.html", context)
    # return JsonResponse({"success": True})


def delete_state(request, id):
    state = State.objects.get(id=id)
    state.delete()
    state_list = State.objects.all()
    context = {
        "state_list": state_list,
        "message": "State Deleted Successfully!!!",
    }
    return render(request, "Admin/State/state.html", context)


# ------------------------------------ CITY -----------------------


def checkcity(request):
    city_name = request.POST.get("city_name").capitalize()

    if City.objects.filter(name=city_name).exists():
        return HttpResponse(
            "<div id='post-data-container' class='error mx-2'>City Name already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='post-data-container' class='success'>City name is available</div>"
        )


def city(request):
    state = State.objects.all()
    city_list = City.objects.all()
    context = {
        "city_list": city_list,
        "message": "City Deleted Successfully!!!",
        "state": state,
    }

    return render(request, "Admin/City/city.html", context)


def addcity(request):

    city_list = City.objects.all()

    if request.method == "POST":

        city_name = request.POST.get("city_name").capitalize()
        state_id = request.POST.get("state_id").capitalize()

        if City.objects.filter(name=city_name).exists():

            message = "City already exists"
            return HttpResponseBadRequest(message)
        state = State.objects.get(id=state_id)
        city = City.objects.create(name=city_name, state=state)
        city.save()
    context = {"city_list": city_list}

    return render(request, "Admin/City/city.html", context)


def editcity(request, id):

    city_name = request.POST.get("city_name").capitalize()

    state_id = request.POST.get("state_id")

    state = State.objects.get(id=state_id)

    city = City.objects.get(id=id)
    city.name = city_name
    city.state = state
    city.save()
    city_list = City.objects.all()
    context = {
        "city_list": city_list,
    }

    return render(request, "Admin/City/city.html", context)


def delete_city(request, id):
    city = City.objects.get(id=id)
    city.delete()

    return redirect("city")


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


def amenities(request):

    amenities_list = Amenities.objects.all()

    context = {
        "amenities_list": amenities_list,
        "message": "Amenities Deleted Successfully!!!",
    }

    return render(request, "Admin/Amenities/amenities.html", context)


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

    ametinies_name = request.POST.get("ametinies_name").capitalize()

    amenities = Amenities.objects.get(id=id)
    amenities.name = ametinies_name
    amenities.save()

    return redirect("amenities")

    # return render(request, "Admin/State/state.html", context)
    # return JsonResponse({"success": True})


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


def arrivals(request):

    arrivals_list = Arrival_Departure.objects.all()

    context = {
        "arrivals_list": arrivals_list,
        "message": "Arrivals Deleted Successfully!!!",
    }

    return render(request, "Admin/ArrivalDeparture/arrival.html", context)


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

    arrivals_name = request.POST.get("arrivals_name").capitalize()

    arrival = Arrival_Departure.objects.get(id=id)
    arrival.name = arrivals_name
    arrival.save()

    return redirect("arrivals")


def delete_arrival(request, id):
    arrival = Arrival_Departure.objects.get(id=id)
    arrival.delete()
    return redirect("arrivals")


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


def amenities(request):

    amenities_list = Amenities.objects.all()

    context = {
        "amenities_list": amenities_list,
        "message": "Amenities Deleted Successfully!!!",
    }

    return render(request, "Admin/Amenities/amenities.html", context)


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

    ametinies_name = request.POST.get("ametinies_name").capitalize()

    amenities = Amenities.objects.get(id=id)
    amenities.name = ametinies_name
    amenities.save()

    return redirect("amenities")

    # return render(request, "Admin/State/state.html", context)
    # return JsonResponse({"success": True})


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


def arrivals(request):

    arrivals_list = Arrival_Departure.objects.all()

    context = {
        "arrivals_list": arrivals_list,
        "message": "Arrivals Deleted Successfully!!!",
    }

    return render(request, "Admin/ArrivalDeparture/arrival.html", context)


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

    arrivals_name = request.POST.get("arrivals_name").capitalize()

    arrival = Arrival_Departure.objects.get(id=id)
    arrival.name = arrivals_name
    arrival.save()

    return redirect("arrivals")


def delete_arrival(request, id):
    arrival = Arrival_Departure.objects.get(id=id)
    arrival.delete()
    return redirect("arrivals")


def delete_city(request, id):
    city = City.objects.get(id=id)
    city.delete()

    return redirect("city")


# ----------------------------------------------------------------------


def add_vehicle(request):

    vehicle_list = Vehicle.objects.all()

    context = {
        "vehicle_list": vehicle_list,
        "message": "vehicle Deleted Successfully!!!",
    }

    return render(request, "Admin/Vehicle/add_vehicle.html", context)


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
    vehicle_list = Vehicle.objects.all()
    context = {
        "vehicle_list": vehicle_list,
        "message": "Vehicle Deleted Successfully!!!",
    }
    return render(request, "Admin/Vehicle/vehicle-list.html", context)


# ----------------------------------------------------------------------


def add_driver(request):

    driver_list = Driver.objects.all()
    vechicle = Vehicle.objects.all()

    context = {
        "driver_list": driver_list,
        "message": "Driver Deleted Successfully!!!",
        "vechicle": vechicle,
    }

    return render(request, "Admin/Driver/add_driver.html", context)


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

        # try:

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
    driver_list = Driver.objects.all()
    context = {
        "driver_list": driver_list,
        "message": "Driver Deleted Successfully!!!",
    }
    return render(request, "Admin/Driver/driver-list.html", context)


# ----------------------------- Meal Plan ------------------------------------


def add_meal_plan(request):

    meal_plan_list = Meal_Plan.objects.all()

    context = {
        "meal_plan_list": meal_plan_list,
        "message": "Meal Plan Deleted Successfully!!!",
    }

    return render(request, "Admin/MealPlan/add_meal_plan.html", context)


def meal_plan(request):

    meal_plan_list = Meal_Plan.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Meal_Plan.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        meal_plan = Meal_Plan.objects.create(name=name)
        meal_plan.save()
    context = {"meal_plan_list": meal_plan_list}

    return render(request, "Admin/MealPlan/meal-list.html", context)


def check_meal_plan(request):
    name = request.POST.get("name").capitalize()
    if Meal_Plan.objects.filter(name=name).exists():
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
    meal_plan_list = Meal_Plan.objects.all()
    context = {
        "meal_plan_list": meal_plan_list,
        "message": "Meal Plan Deleted Successfully!!!",
    }
    return render(request, "Admin/MealPlan/meal-list.html", context)


# -------------------------------------- Extra Meal -------------------


def extrameal(request):
    return render(request, "Admin/ExtraMeal/extra_meal.html")

def add_extrameal(request):
    return render(request, "Admin/ExtraMeal/add_extrameal.html")


# ----------------------------- Hotel Category ------------------------------------


def add_hotel_category(request):

    hotel_category_list = Hotel_Category.objects.all()

    context = {
        "hotel_category_list": hotel_category_list,
        "message": "Hotel Category Deleted Successfully!!!",
    }

    return render(request, "Admin/HotelCategory/add_hotel_category.html", context)


def hotel_category(request):

    hotel_category_list = Hotel_Category.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Hotel_Category.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        hotel_category = Hotel_Category.objects.create(name=name)
        hotel_category.save()
    context = {"hotel_category_list": hotel_category_list}

    return render(request, "Admin/HotelCategory/hotel_category-list.html", context)


def check_hotel_category(request):
    name = request.POST.get("name").capitalize()
    if Hotel_Category.objects.filter(name=name).exists():
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
    hotel_category_list = Hotel_Category.objects.all()
    context = {
        "hotel_category_list": hotel_category_list,
        "message": "Hotel Category Deleted Successfully!!!",
    }
    return render(request, "Admin/HotelCategory/hotel_category-list.html", context)


# ----------------------------- Ferry Class ------------------------------------


def add_ferry_class(request):

    ferry_class_list = Ferry_Class.objects.all()

    context = {
        "ferry_class_list": ferry_class_list,
        "message": "Ferry Class Deleted Successfully!!!",
    }

    return render(request, "Admin/FerryClass/add_ferry_class.html", context)


def ferry_class(request):

    ferry_class_list = Ferry_Class.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Ferry_Class.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        ferry_class = Ferry_Class.objects.create(name=name)
        ferry_class.save()
    context = {"ferry_class_list": ferry_class_list}

    return render(request, "Admin/FerryClass/ferry_class-list.html", context)


def check_ferry_class(request):
    name = request.POST.get("name").capitalize()
    if Ferry_Class.objects.filter(name=name).exists():
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
    ferry_class_list = Ferry_Class.objects.all()
    context = {
        "ferry_class_list": ferry_class_list,
        "message": "Ferry Class Deleted Successfully!!!",
    }
    return render(request, "Admin/FerryClass/ferry_class-list.html", context)


# ----------------------------- Extra Expense Type ------------------------------------


def add_extra_service(request):

    extra_service_list = Expense_servive_type.objects.all()

    context = {
        "extra_service_list": extra_service_list,
        "message": "Extra Service Type Deleted Successfully!!!",
    }

    return render(request, "Admin/ExtraServiceType/add_extra_service.html", context)


def extra_service(request):

    extra_service_list = Expense_servive_type.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        remarks = request.POST.get("remarks")

        if Expense_servive_type.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        extra_service = Expense_servive_type.objects.create(name=name, remarks=remarks)
        extra_service.save()
    context = {"extra_service_list": extra_service_list}

    return render(request, "Admin/ExtraServiceType/extra_service-list.html", context)


def check_extra_service(request):
    name = request.POST.get("name").capitalize()
    if Expense_servive_type.objects.filter(name=name).exists():
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
            extra_service = Expense_servive_type.objects.get(id=id)
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
    extra_service_list = Expense_servive_type.objects.all()
    context = {
        "extra_service_list": extra_service_list,
        "message": "Extra Service Type Deleted Successfully!!!",
    }

    return render(request, "Admin/ExtraServiceType/add_extra_service.html", context)


def delete_extra_service(request, id):
    extra_service = Expense_servive_type.objects.get(id=id)
    extra_service.delete()
    messages.success(request, "Extra Service Type Deleted log for alertify!!!")
    extra_service_list = Expense_servive_type.objects.all()
    context = {
        "extra_service_list": extra_service_list,
        "message": "Extra Service Type Deleted Successfully!!!",
    }
    return render(request, "Admin/ExtraServiceType/extra_service-list.html", context)


# ----------------------------- Extra Meal Price ------------------------------------


def add_extra_meal_price(request):

    extra_meal_price_list = Extra_Meal_Price.objects.all()

    context = {
        "extra_meal_price_list": extra_meal_price_list,
        "message": "Extra Meal Price Deleted Successfully!!!",
    }

    return render(request, "Admin/ExtraMealPrice/add_extra_meal_price.html", context)


def extra_meal_price(request):

    extra_meal_price_list = Extra_Meal_Price.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        adult = request.POST.get("adult")
        child = request.POST.get("child")
        infant = request.POST.get("infant")

        if Extra_Meal_Price.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        extra_meal_price = Extra_Meal_Price.objects.create(
            name=name, adult=adult, child=child, infant=infant
        )
        extra_meal_price.save()
    context = {"extra_meal_price_list": extra_meal_price_list}

    return render(request, "Admin/ExtraMealPrice/extra_meal_price-list.html", context)


def check_extra_meal_price(request):
    name = request.POST.get("name").capitalize()
    if Extra_Meal_Price.objects.filter(name=name).exists():
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
    extra_meal_price_list = Extra_Meal_Price.objects.all()
    context = {
        "extra_meal_price_list": extra_meal_price_list,
        "message": "Extra Meal Price Deleted Successfully!!!",
    }
    return render(request, "Admin/ExtraMealPrice/extra_meal_price-list.html", context)


# ----------------------------- Flight ------------------------------------


def add_flight(request):

    flight_list = Flight.objects.all()

    context = {
        "flight_list": flight_list,
        "message": "Flight Deleted Successfully!!!",
    }

    return render(request, "Admin/Flight/add_flight.html", context)


def flight(request):

    flight_list = Flight.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        image = request.FILES.get("image")

        if Flight.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        flight = Flight.objects.create(name=name, image=image)
        flight.save()
    context = {"flight_list": flight_list}

    return render(request, "Admin/Flight/flight-list.html", context)


def check_flight(request):
    name = request.POST.get("name").capitalize()
    if Flight.objects.filter(name=name).exists():
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
    flight_list = Flight.objects.all()
    context = {
        "flight_list": flight_list,
        "message": "Flight Deleted Successfully!!!",
    }
    return render(request, "Admin/Flight/flight-list.html", context)


# ----------------------------- Currency ------------------------------------


def add_currency(request):

    currency_list = Currency.objects.all()

    context = {
        "currency_list": currency_list,
        "message": "Currency Deleted Successfully!!!",
    }

    return render(request, "Admin/Currency/add_currency.html", context)


def currency(request):

    currency_list = Currency.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        value = request.POST.get("value")
        base_currency = request.POST.get("base_currency")

        if Currency.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        currency = Currency.objects.create(
            name=name, value=value, base_currency=base_currency
        )
        currency.save()
    context = {"currency_list": currency_list}

    return render(request, "Admin/Currency/currency-list.html", context)


def check_currency(request):
    name = request.POST.get("name").capitalize()
    if Currency.objects.filter(name=name).exists():
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
    currency_list = Currency.objects.all()
    context = {
        "currency_list": currency_list,
        "message": "Currency Deleted Successfully!!!",
    }
    return render(request, "Admin/Currency/currency-list.html", context)


# ----------------------------- Lead Source ------------------------------------


def add_lead_source(request):

    lead_source_list = Lead_source.objects.all()

    context = {
        "lead_source_list": lead_source_list,
        "message": "Lead Source Deleted Successfully!!!",
    }

    return render(request, "Admin/LeadSource/add_lead_source.html", context)


def lead_source(request):

    lead_source_list = Lead_source.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Lead_source.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        lead_source = Lead_source.objects.create(name=name)
        lead_source.save()
    context = {"lead_source_list": lead_source_list}

    return render(request, "Admin/LeadSource/lead_source-list.html", context)


def check_lead_source(request):
    name = request.POST.get("name").capitalize()
    if Lead_source.objects.filter(name=name).exists():
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
    lead_source_list = Lead_source.objects.all()
    context = {
        "lead_source_list": lead_source_list,
        "message": "Lead Source Deleted Successfully!!!",
    }
    return render(request, "Admin/LeadSource/lead_source-list.html", context)


# ----------------------------- Banks ------------------------------------


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


# def edit_bank(request, id):
#     if request.method == "POST":
#         try:
#             bank_name = request.POST.get("bank_name").capitalize()
#             account_details = request.POST.get("account_details")
#             country = request.POST.get("country")
#             state = request.POST.get("state")
#             city = request.POST.get("city")
#             zip = request.POST.get("zip")
#             address = request.POST.get("address")
#             currency = request.POST.get("currency")
#             bank = Bank.objects.get(id=id)
#             bank.bank_name = bank_name
#             bank.account_details = account_details
#             bank.country = country
#             bank.state = state
#             bank.city = city
#             bank.zip = zip
#             bank.address = address
#             bank.currency = currency
#             bank.save()
#             messages.success(request, "Bank updated successfully")
#             return redirect("add_bank")
#         except Exception as e:
#             messages.error(request, f"Error occurred: {e}")
#             return redirect("add_bank")
#     else:
#         pass
#     bank_list = Bank.objects.all()
#     context = {
#         "bank_list": bank_list,
#         "message": "Bank Deleted Successfully!!!",
#     }

#     return render(request, "Admin/Bank/add_bank.html", context)


def delete_bank(request, id):
    bank = Bank.objects.get(id=id)
    bank.delete()
    messages.success(request, "Bank Deleted log for alertify!!!")
    bank_list = Bank.objects.all()
    context = {
        "bank_list": bank_list,
        "message": "Bank Deleted Successfully!!!",
    }
    return render(request, "Admin/Bank/bank-list.html", context)


# ----------------------------- Destination ------------------------------------


def add_destination(request):

    destination_list = Destination.objects.all()
    country = Country.objects.all()

    context = {
        "destination_list": destination_list,
        "country": country,
        "message": "Destination Deleted Successfully!!!",
    }

    return render(request, "Admin/Destination/add_destination.html", context)


def destination(request):

    destination_list = Destination.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        country_id = request.POST.get("country_id")

        country = Country.objects.get(id=country_id)

        if Destination.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        destination = Destination.objects.create(name=name, country=country)
        destination.save()
    context = {"destination_list": destination_list}

    return render(request, "Admin/Destination/destination-list.html", context)


def check_destination(request):
    name = request.POST.get("name").capitalize()
    if Destination.objects.filter(name=name).exists():
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
    destination_list = Destination.objects.all()
    context = {
        "destination_list": destination_list,
        "message": "Destination Deleted Successfully!!!",
    }
    return render(request, "Admin/Destination/destination-list.html", context)


# ----------------------------- Restaurent Location ------------------------------------


def add_restaurentlocation(request):

    restaurentlocation_list = Restaurent_location.objects.all()
    destination = Destination.objects.all()

    context = {
        "restaurentlocation_list": restaurentlocation_list,
        "destination": destination,
        "message": "Restaurent Location Deleted Successfully!!!",
    }

    return render(request, "Admin/RestaurentLocation/add_restaurent_location.html", context)


def restaurentlocation(request):
    restaurentlocation_list = Restaurent_location.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        destination_id = request.POST.get("destination_id")

        destination = Destination.objects.get(id=destination_id)

        if Restaurent_location.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        restaurentlocation = Restaurent_location.objects.create(
            name=name, destination=destination
        )
        restaurentlocation.save()
    context = {"restaurentlocation_list": restaurentlocation_list}

    return render(request, "Admin/RestaurentLocation/restaurent_location-list.html", context)


def check_restaurentlocation(request):
    name = request.POST.get("name").capitalize()
    if Restaurent_location.objects.filter(name=name).exists():
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
    restaurentlocation_list = Restaurent_location.objects.all()
    context = {
        "restaurentlocation_list": restaurentlocation_list,
        "message": "Restaurant Location Deleted Successfully!!!",
    }
    return render(request, "Admin/RestaurentLocation/restaurent_location-list.html", context)



# ----------------------------- Restaurent Type ------------------------------------


def add_restaurenttype(request):

    restaurenttype_list = Restaurent_type.objects.all()

    context = {
        "restaurenttype_list": restaurenttype_list,
        "message": "Restaurent Type Deleted Successfully!!!",
    }

    return render(request, "Admin/RestaurentType/add_restaurent_type.html", context)


def restaurenttype(request):
    restaurenttype_list = Restaurent_type.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()

        if Restaurent_type.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        restaurenttype = Restaurent_type.objects.create(name=name)
        restaurenttype.save()
    context = {"restaurenttype_list": restaurenttype_list}

    return render(request, "Admin/RestaurentType/restaurent_type-list.html", context)


def check_restaurenttype(request):
    name = request.POST.get("name").capitalize()
    if Restaurent_type.objects.filter(name=name).exists():
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
    restaurenttype_list = Restaurent_type.objects.all()
    context = {
        "restaurenttype_list": restaurenttype_list,
        "message": "Restaurant Type Deleted Successfully!!!",
    }
    return render(request, "Admin/Restaurent Type/restaurent_type-list.html", context)



# ----------------------------- Special Days ------------------------------------


def add_specialdays(request):

    specialdays_list = Special_days.objects.all()

    context = {
        "specialdays_list": specialdays_list,
        "message": "Special Days Deleted Successfully!!!",
    }

    return render(request, "Admin/SpecialDays/add_special_days.html", context)


def specialdays(request):
    specialdays_list = Special_days.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        block_out_from_date = request.POST.get("block_out_from_date")
        block_out_to_date = request.POST.get("block_out_to_date")

        if Special_days.objects.filter(name=name).exists():
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
    if Special_days.objects.filter(name=name).exists():
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
    specialdays_list = Special_days.objects.all()
    context = {
        "specialdays_list": specialdays_list,
        "message": "Special Days Deleted Successfully!!!",
    }
    return render(request, "Admin/Special Days/special_days-list.html", context)



# ----------------------------- Room Type ------------------------------------


def add_roomtype(request):

    roomtype_list = Room_type.objects.all()

    context = {
        "roomtype_list": roomtype_list,
        "message": "Room Type Deleted Successfully!!!",
    }

    return render(request, "Admin/RoomType/add_roomtype.html", context)


def roomtype(request):

    roomtype_list = Room_type.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        remarks = request.POST.get("remarks")

        if Room_type.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        roomtype = Room_type.objects.create(name=name, remarks=remarks)
        roomtype.save()
    context = {"roomtype_list": roomtype_list}

    return render(request, "Admin/RoomType/roomtype-list.html", context)


def check_roomtype(request):
    name = request.POST.get("name").capitalize()
    if Room_type.objects.filter(name=name).exists():
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
    roomtype_list = Room_type.objects.all()
    context = {
        "roomtype_list": roomtype_list,
        "message": "Room Type Deleted Successfully!!!",
    }
    return render(request, "Admin/RoomType/roomtype-list.html", context)


# ----------------------------- Hotel Location ------------------------------------


def add_hotellocation(request):

    hotellocation_list = Hotel_location.objects.all()
    destination = Destination.objects.all()

    context = {
        "hotellocation_list": hotellocation_list,
        "destination": destination,
        "message": "Hotel Location Deleted Successfully!!!",
    }

    return render(request, "Admin/HotelLocation/add_hotel_location.html", context)


def hotellocation(request):
    hotellocation_list = Hotel_location.objects.all()
    if request.method == "POST":

        name = request.POST.get("name").capitalize()
        destination_id = request.POST.get("destination_id")

        destination = Destination.objects.get(id=destination_id)

        if Hotel_location.objects.filter(name=name).exists():
            return HttpResponseBadRequest("WRONG")
        hotellocation = Hotel_location.objects.create(
            name=name, destination=destination
        )
        hotellocation.save()
    context = {"hotellocation_list": hotellocation_list}

    return render(request, "Admin/HotelLocation/hotel_location-list.html", context)


def check_hotellocation(request):
    name = request.POST.get("name").capitalize()
    if Hotel_location.objects.filter(name=name).exists():
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



def add_visa(request):

    visa_list = Visa.objects.all()
    currency = Currency.objects.all()

    context = {
        "visa_list": visa_list,
        "message": "Visa Deleted Successfully!!!",
        "currency":currency
    }

    return render(request, "Admin/Visa/add_visa.html", context)


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
    visa_list = Visa.objects.all()
    context = {
        "visa_list": visa_list,
        "message": "Visa Deleted Successfully!!!",
    }
    return render(request, "Admin/Visa/visa-list.html", context)



# ----------------------------- Transfer Location ------------------------------------



def add_transfer_location(request):

    transfer_location_list = Transfer_location.objects.all()

    context = {
        "transfer_location_list": transfer_location_list,
        "message": "Transfer Location Deleted Successfully!!!",
    }

    return render(request, "Admin/TransferLocation/add_Transfer_location.html", context)


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
    transfer_location_list = Transfer_location.objects.all()
    context = {
        "transfer_location_list": transfer_location_list,
        "message": "Transfer Location Deleted Successfully!!!",
    }
    return render(request, "Admin/TransferLocation/Transfer_location-list.html", context)


from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard", index, name="home"),
    # ----------------------COUNTRY----------------
    path("add_Country", add_Country, name="add_Country"),
    path("country", country, name="country"),
    path("checkusername", check_country, name="checkusername"),
    path("edit_Country/<int:id>/", edit_Country, name="edit_Country"),
    path("delete_country/<int:id>/", delete_country, name="delete_country"),
    # -------------------STATE--------------------------
    path("state", state, name="state"),
    path("Addstate", addstate, name="addstate"),
    path("checkstate", check_state, name="checkstates"),
    path("Edit/State/<int:id>/", editstate, name="editstate"),
    path("delete_state/<int:id>/", delete_state, name="delete_state"),
    # --------------------CITY -------------------------------
    path("checkcity", checkcity, name="checkcity"),
    path("City", city, name="city"),
    path("Add/City", addcity, name="addcity"),
    path("Edit/City/<int:id>/", editcity, name="editcity"),
    path("Delte/City/<int:id>/", delete_city, name="delete_city"),
    # ------------------------VEHICLE--------------------------
    path("add_vehicle", add_vehicle, name="add_vehicle"),
    path("vehicle", vehicle, name="vehicle"),
    path("edit_vehicle/<int:id>/", edit_vehicle, name="edit_vehicle"),
    path("delete_vehicle/<int:id>/", delete_vehicle, name="delete_vehicle"),
    # ------------------------Driver--------------------------
    path("add_driver", add_driver, name="add_driver"),
    path("driver", driver, name="driver"),
    path("edit_driver/<int:id>/", edit_driver, name="edit_driver"),
    path(
        "get_transfer_capacity/<int:vehicle_id>/",
        get_transfer_capacity,
        name="get_transfer_capacity",
    ),
    path("delete_driver/<int:id>/", delete_driver, name="delete_driver"),
    # -------------------------- Meal plan ----------------------
    path("add_meal_plan", add_meal_plan, name="add_meal_plan"),
    path("meal_plan", meal_plan, name="meal_plan"),
    path("checkmealplanname", check_meal_plan, name="checkmealplanname"),
    path("edit_meal_plan/<int:id>/", edit_meal_plan, name="edit_meal_plan"),
    path("delete_meal_plan/<int:id>/", delete_meal_plan, name="delete_meal_plan"),
    # -------------------------- Hotel Category ----------------------
    path("add_hotel_category", add_hotel_category, name="add_hotel_category"),
    path("hotel_category", hotel_category, name="hotel_category"),
    path("checkhotelcategoryname", check_hotel_category, name="checkhotelcategoryname"),
    path(
        "edit_hotel_category/<int:id>/", edit_hotel_category, name="edit_hotel_category"
    ),
    path(
        "delete_hotel_category/<int:id>/",
        delete_hotel_category,
        name="delete_hotel_category",
    ),
    # -------------------------- Ferry Class ----------------------
    path("add_ferry_class", add_ferry_class, name="add_ferry_class"),
    path("ferry_class", ferry_class, name="ferry_class"),
    path("checkferryclassname", check_ferry_class, name="checkferryclassname"),
    path("edit_ferry_class/<int:id>/", edit_ferry_class, name="edit_ferry_class"),
    path("delete_ferry_class/<int:id>/", delete_ferry_class, name="delete_ferry_class"),
    # -------------------------- Extra Service Type ----------------------
    path("add_extra_service", add_extra_service, name="add_extra_service"),
    path("extra_service", extra_service, name="extra_service"),
    path("checkextraservicename", check_extra_service, name="checkextraservicename"),
    path("edit_extra_service/<int:id>/", edit_extra_service, name="edit_extra_service"),
    path(
        "delete_extra_service/<int:id>/",
        delete_extra_service,
        name="delete_extra_service",
    ),
    # -------------------------- Extra Meal Price ----------------------
    path("add_extra_meal_price", add_extra_meal_price, name="add_extra_meal_price"),
    path("extra_meal_price", extra_meal_price, name="extra_meal_price"),
    path(
        "checkextramealpricename",
        check_extra_meal_price,
        name="checkextramealpricename",
    ),
    path(
        "edit_extra_meal_price/<int:id>/",
        edit_extra_meal_price,
        name="edit_extra_meal_price",
    ),
    path(
        "delete_extra_meal_price/<int:id>/",
        delete_extra_meal_price,
        name="delete_extra_meal_price",
    ),
    # -------------------------- Flight ----------------------
    path("add_flight", add_flight, name="add_flight"),
    path("flight", flight, name="flight"),
    path("checkflightname", check_flight, name="checkflightname"),
    path("edit_flight/<int:id>/", edit_flight, name="edit_flight"),
    path("delete_flight/<int:id>/", delete_flight, name="delete_flight"),
    # -------------------------- Currency ----------------------
    path("add_currency", add_currency, name="add_currency"),
    path("currency", currency, name="currency"),
    path("checkcurrencyname", check_currency, name="checkcurrencyname"),
    path("edit_currency/<int:id>/", edit_currency, name="edit_currency"),
    path("delete_currency/<int:id>/", delete_currency, name="delete_currency"),
    # -------------------------- Lead Source ----------------------
    path("add_lead_source", add_lead_source, name="add_lead_source"),
    path("lead_source", lead_source, name="lead_source"),
    path("checklead_sourcename", check_lead_source, name="checklead_sourcename"),
    path("edit_lead_source/<int:id>/", edit_lead_source, name="edit_lead_source"),
    path("delete_lead_source/<int:id>/", delete_lead_source, name="delete_lead_source"),
    # -------------------------- Bank ----------------------
    path("add_bank", add_bank, name="add_bank"),
    path("get_states", get_states, name="get_states"),
    path("get_city", get_city, name="get_city"),
    path("bank", bank, name="bank"),
    # path("edit_bank/<int:id>/", edit_bank, name="edit_bank"),
    path("delete_bank/<int:id>/", delete_bank, name="delete_bank"),
    # -------------------------- Destination ----------------------
    path("add_destination", add_destination, name="add_destination"),
    path("destination", destination, name="destination"),
    path("checkdestinationname", check_destination, name="checkdestinationname"),
    path("edit_destination/<int:id>/", edit_destination, name="edit_destination"),
    path("delete_destination/<int:id>/", delete_destination, name="delete_destination"),
    # -------------------------- Restaurent Location ----------------------
    path(
        "add_restaurentlocation", add_restaurentlocation, name="add_restaurentlocation"
    ),
    path("restaurentlocation", restaurentlocation, name="restaurentlocation"),
    path(
        "checkrestaurentlocationname",
        check_restaurentlocation,
        name="checkrestaurentlocationname",
    ),
    path(
        "edit_restaurentlocation/<int:id>/",
        edit_restaurentlocation,
        name="edit_restaurentlocation",
    ),
    path(
        "delete_restaurentlocation/<int:id>/",
        delete_restaurentlocation,
        name="delete_restaurentlocation",
    ),
    # -------------------------- Restaurent Type ----------------------
    path("add_restaurenttype", add_restaurenttype, name="add_restaurenttype"),
    path("restaurenttype", restaurenttype, name="restaurenttype"),
    path(
        "checkrestaurenttypename", check_restaurenttype, name="checkrestaurenttypename"
    ),
    path(
        "edit_restaurenttype/<int:id>/", edit_restaurenttype, name="edit_restaurenttype"
    ),
    path(
        "delete_restaurenttype/<int:id>/",
        delete_restaurenttype,
        name="delete_restaurenttype",
    ),
    # -------------------------- Special Days ----------------------
    path("add_specialdays", add_specialdays, name="add_specialdays"),
    path("specialdays", specialdays, name="specialdays"),
    path("checkspecialdaysname", check_specialdays, name="checkspecialdaysname"),
    path("edit_specialdays/<int:id>/", edit_specialdays, name="edit_specialdays"),
    path("delete_specialdays/<int:id>/", delete_specialdays, name="delete_specialdays"),
    # -------------------------- Room Type ----------------------
    path("add_roomtype", add_roomtype, name="add_roomtype"),
    path("roomtype", roomtype, name="roomtype"),
    path("checkroomtypename", check_roomtype, name="checkroomtypename"),
    path("edit_roomtype/<int:id>/", edit_roomtype, name="edit_roomtype"),
    path("delete_roomtype/<int:id>/", delete_roomtype, name="delete_roomtype"),
    # -------------------------- Hotel Location ----------------------
    path("add_hotellocation", add_hotellocation, name="add_hotellocation"),
    path("hotellocation", hotellocation, name="hotellocation"),
    path("checkhotellocationname", check_hotellocation, name="checkhotellocationname"),
    path("edit_hotellocation/<int:id>/", edit_hotellocation, name="edit_hotellocation"),
    path(
        "delete_hotellocation/<int:id>/",
        delete_hotellocation,
        name="delete_hotellocation",
    ),
    # -------------------------- Visa ----------------------
    path("add_visa", add_visa, name="add_visa"),
    path("visa", visa, name="visa"),
    path("checkvisaname", check_visa, name="checkvisaname"),
    path("edit_visa/<int:id>/", edit_visa, name="edit_visa"),
    path("delete_visa/<int:id>/", delete_visa, name="delete_visa"),
    # -------------------------- Transfer Location ----------------------
    path("add_transfer_location", add_transfer_location, name="add_transfer_location"),
    path("transfer_location", transfer_location, name="transfer_location"),
    path(
        "checktransfer_locationname",
        check_transfer_location,
        name="checktransfer_locationname",
    ),
    path(
        "edit_transfer_location/<int:id>/",
        edit_transfer_location,
        name="edit_transfer_location",
    ),
    path(
        "delete_transfer_location/<int:id>/",
        delete_transfer_location,
        name="delete_transfer_location",
    ),
    
        # -------------------------- Restaurant ----------------------
    path("restaurant", restaurant, name="restaurant"),
    path("add_restaurant", add_restaurant, name="add_restaurant"),
    path("delete_restaurant/<int:id>/", delete_restaurant, name="delete_restaurant"),
    path("edit_restaurant/<int:id>/", edit_restaurant, name="edit_restaurant"),
    path('get-restaurant-locations/', get_restaurant_locations, name='get-restaurant-locations'),
    
    # ------------------------Guide--------------------------
    path("add_guide", add_guide, name="add_guide"),
    path("guide", guide, name="guide"),
    # path("edit_guide/<int:id>/", edit_guide, name="edit_guide"),
    path("delete_guide/<int:id>/", delete_guide, name="delete_guide"),
    # ------------------------- Amenities -----------------------------
    path("checkamenities", checkamenities, name="checkamenities"),
    path("Amenities", amenities, name="amenities"),
    path("Add/Amenities", addamenities, name="addamenities"),
    path("Edit/Amenities/<int:id>/", editamenities, name="editamenities"),
    path("delete_amenities/<int:id>/", delete_amenities, name="delete_amenities"),
    # ------------------------- Arrivals -----------------------------
    path("checkarrivals", checkarrivals, name="checkarrivals"),
    path("Arrivals", arrivals, name="arrivals"),
    path("Add/Arrivals", addarrivals, name="addarrivals"),
    path("Edit/Arrival/<int:id>/", editarrival, name="editarrival"),
    path("Delete/Arrival/<int:id>/", delete_arrival, name="delete_arrival"),
    # ------------------------- Hotel -----------------------------
    
    path("hotel", hotel, name="hotel"),
    path("add_hotel", add_hotel, name="add_hotel"),
    path("get_destination", get_destination, name="get_destination"),
    path("delete_hotel/<int:id>/", delete_hotel, name="delete_hotel"),
    # -------------------------- Extra Meal  ----------------------
    path("check_extrameal", check_extrameal, name="check_extrameal"),
    path("Extra/Meal", extrameal, name="extrameal"),
    path("Add/Extra/Meal", add_extrameal, name="add_extrameal"),
    path("Edit/Extra/Meal/<int:id>/", edit_extra_meal, name="edit_extra_meal"),
    
    # ---------------------------- Sightseeing ----------------------
    
    path("sightseeing", sightseeing, name="sightseeing"),
    path("Add/sightseeing", add_sightseeing, name="add_sightseeing"),
    path("delete_sightseeing/<int:id>/", delete_sightseeing, name="delete_sightseeing"),
    # ---------------------------- Supplier ----------------------
    path("supplier", supplier, name="supplier"),
    path("Add/supplier", add_supplier, name="add_supplier"),
    path("delete_supplier/<int:id>/", delete_supplier, name="delete_supplier"),
    # ---------------------------- Transfer ----------------------
    path("transfer", transfer, name="transfer"),
    path("Add/transfer", add_transfer, name="add_transfer"),
    path("delete_transfer/<int:id>/", delete_transfer, name="delete_transfer"),
    # ---------------------------- Itinerary ----------------------
    path("add_itinerary", add_itinerary, name="add_itinerary"),
    path("itinerary", itinerary, name="itinerary"),
    path("delete_itinerary/<int:id>/", delete_itinerary, name="delete_itinerary"),
    # ---------------------------- Documents -------------------------
    path("documents", documents, name="documents"),
    path("add_document", add_document, name="add_document"),
    # path("view_document/<int:id>/", view_all_document, name="view_document"),
    path("Edit/Document/<int:id>/", edit_document, name="edit_document"),
    path("delete_document/<int:id>/", delete_document, name="delete_document"),
    # -------------------------- Role Permission ----------------------
    path("add_role", add_role, name="add_role"),
    path("role", role, name="role"),
    path("checkrolename", check_role, name="checkrolename"),
    path(
        "edit_role/<int:id>/", edit_role, name="edit_role"
    ),
    path(
        "delete_role/<int:id>/",
        delete_role,
        name="delete_role",
    ),
    # ------------------------------- ADMIN ------------------------------------------
    
    path("add_user", add_user, name="add_user"),
    path("user", user, name="user"),
    
    # --------------------------------- QUERY ------------------------------
    
    path("newquerylist", newquerylist, name="newquerylist"),
    path("allquerylist", allquerylist, name="allquerylist"),
    path("connectedquerylist", connectedquerylist, name="connectedquerylist"),
    path("quatationquerylist", quatationquerylist, name="quatationquerylist"),
    path("paymentprocessquerylist", paymentprocessquerylist, name="paymentprocessquerylist"),
    path("paymentdonequerylist", paymentdonequerylist, name="paymentdonequerylist"),
    path("completedquery", completedquerylist, name="completedquery"),
    path("lostquery", lostquerylist, name="lostquery"),
    path("addquery", addquery, name="addquery"),
    path("editquery/<int:id>/", editquery, name="editquery"),
    path('lead/<int:id>/update/', lead_status_update, name='lead_status_update'),
    path('op/<int:id>/update/', op_update, name='op_update'),
    # path('add_quatation/<int:id>/', add_quatation, name='add_quatation'),
    path('attach_quatation/<int:id>/', attach_quotation, name='attach_quatation'),
    path('add_notes/<int:id>/', add_notes, name='add_notes'),
    path('add_followup/<int:id>/', add_followup, name='add_followup'),
    path('generate/paymentlink/<int:id>/', payment_link, name='payment_link'),
    path('Check/Payment/Status/<int:id>/', payment_status, name='payment_status'),
    path('make_click_to_call/<int:id>/', make_click_to_call, name='make_click_to_call'),
    
    
]

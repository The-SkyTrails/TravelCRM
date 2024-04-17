from django.shortcuts import render , redirect
from Admin.models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages




def CustomLoginView(request):
    if request.user.is_authenticated:
        return redirect("home")
    # if request.user.user_type == 'Admin':
    #     return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(username=username)

            if check_password(password, user.password):
                # user_type = user.user_type
                # if user_type == "Admin":
                user.is_logged_in = "Yes"
                user.save()
                login(request, user)
                return redirect("home")
            # else:
            #         messages.error(request, "You are not authorized to login.")
            #         return redirect("login")
            else:
                messages.error(request, "Username and Password Incorrect")
                return redirect("login")

        except CustomUser.DoesNotExist:
            messages.error(request, "User Does Not Exist")
            return redirect("login")
    return render(request, "Login/login.html")
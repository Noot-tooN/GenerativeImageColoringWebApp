from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html", {})
    else: # POST
        email = request.POST.get("email", "")
        pas = request.POST.get("password", "")
        if email == "" or pas == "":
            return render(request, "login.html", {"login_err_status": "Either email or password were not provided"})
        
        
        user = authenticate(email=email, password=pas)
        if user is None:
            return render(request, "login.html", {"login_err_status": "Invalid credentials!"})
        
        login(request, user)
        
        if 'next' in request.GET:
            return redirect(request.GET.get("next"))

        return redirect("home_page")

def register_view(request):
    if request.method == "GET":
        return render(request, "register.html", {})
    else: # POST
        email = request.POST.get("email", "")
        pas = request.POST.get("password", "")
        if email == "" or pas == "":
            return render(request, "register.html", {"register_err_status": "Either email or password were not provided"})
        
        if CustomUser.objects.filter(email=email).exists():
            return render(request, "register.html", {"register_err_status": "User already exists!"})

        cu = CustomUser.objects.create_user(email=email, password=pas, permission_level=0)
        cu.save()

        return render(request, "register.html", {"register_status": "Successfully registered! You can login now!"})

@login_required()
def profile_view(request):
    if request.method == "GET":
        return render(request, "profile.html", {})
    else:
        new_permission_lvl = request.POST.get("new_permission_level", "")
        if new_permission_lvl == "" or int(new_permission_lvl) < 0 or int(new_permission_lvl) >2:
            return render(request, "profile.html", {"profile_err_status": "Invalid value for permission level!"})
        
        user = CustomUser.objects.filter(email=request.user.email)[0]

        if int(new_permission_lvl) == int(user.permission_level):
            return render(request, "profile.html", {"profile_err_warning": "Permission is already at the same level!"})

        user.permission_level = new_permission_lvl
        user.save()
        return redirect("profile_view")

@login_required()
def logout_view(request):
    logout(request)
    return redirect("home_page")

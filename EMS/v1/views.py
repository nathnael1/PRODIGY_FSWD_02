from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect,HttpResponseForbidden
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return HttpResponseForbidden("User does not exist")
        return render(request,"index.html",{"user":user})
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        full_name = request.POST.get("fullName")
        password = request.POST.get("password")
        password_repeat = request.POST.get("password_repeat")
        email = request.POST.get("email")
        image = request.FILES.get("image")
        birth_date = request.POST.get("date")
        admin_key = request.POST.get("adminKey")
        user = User.objects.filter(username=username).first()
        errors = {}

        if user:
            errors["error"] = "User already exists"
        elif not all([username, full_name, password, email, image, birth_date]):
            errors["error"] = "All fields are required"
        elif len(password) < 8:
            errors["error"] = "Password must be at least 8 characters"
        elif password != password_repeat:
            errors["error"] = "Passwords do not match"

        if errors:
            return render(request, 'signup.html', {"errors": errors})
        if admin_key == "1234":
            is_admin = True
        if not admin_key:
            is_admin = False
        user = User(
            username = username,
            full_name = full_name,
            email = email,

            birth_date = birth_date,
            admin = is_admin
        )
        user.image = image
        user.set_password(password)
        user.save()
        messages.success(request, "Registered Successfully")
        return HttpResponseRedirect(reverse("login"))

    return render(request,"signup.html")
def login(request):
    errors = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            errors["error"] = "Username and password are required."   
            return render(request, "login.html", {"errors": errors})
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                errors["error"] = "Invalid credentials."
    
            return render(request, "login.html", {"errors": errors})
    elif request.method == "GET":
        
        if request.user.is_authenticated:
            logout(request)
        if messages.get_messages(request):
            return render(request,"login.html")
        else:
            return render(request,"login.html")
@csrf_exempt
def edit(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)
        data = request.POST
        full_name = data.get("full_name")
        email = data.get("email")
        username = data.get("username")
        birth_date = data.get("birth_date")
        image = request.FILES.get("image")
        if full_name:
            user.full_name = full_name
        if email:
            user.email = email
        if birth_date:
            try:
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
                print("recived birthdate",{birth_date})
                user.birth_date = birth_date
            except ValueError:
                return JsonResponse({"error": "Invalid date format. Expected format: 'YYYY-MM-DD'."})
        if username:
            user.username = username
        if image:
            user.image = image
        user.save()
        return JsonResponse({"success": "Profile updated successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
def adminmanager(request):
    if request.user.is_authenticated:
        if request.user.admin:
            user_list = User.objects.all().order_by('-id')
            paginator = Paginator(user_list, 10)  
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'adminmanager.html', {'page_obj': page_obj})
        else:
            return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))

def addUser(request):
    if request.user.admin:
        if request.method == "POST":
            username = request.POST.get("username")
            full_name = request.POST.get("fullName")
            password = request.POST.get("password")
            password_repeat = request.POST.get("password_repeat")
            email = request.POST.get("email")
            image = request.FILES.get("image")
            birth_date = request.POST.get("date")
            admin_key = request.POST.get("adminKey")
            user = User.objects.filter(username=username).first()
            errors = {}

            if user:
                errors["error"] = "User already exists"
            elif not all([username, full_name, password, email, image, birth_date]):
                errors["error"] = "All fields are required"
            elif len(password) < 8:
                errors["error"] = "Password must be at least 8 characters"
            elif password != password_repeat:
                errors["error"] = "Passwords do not match"

            if errors:
                return render(request, 'signup.html', {"errors": errors})
            if admin_key == "1234":
                is_admin = True
            if not admin_key:
                is_admin = False
            user = User(
                username = username,
                full_name = full_name,
                email = email,

                birth_date = birth_date,
                admin = is_admin
            )
            user.image = image
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse("adminmanager"))
        return render(request,'add.html')
    else:
        return HttpResponseRedirect(reverse("index"))
@csrf_exempt
def editUser(request, username):
    if not request.user.admin:
        return JsonResponse({"error": "Unauthorized"}, status=403)
    try:
         user = get_object_or_404(User, username=username)
    except User.DoesNotExist:
        return HttpResponseForbidden("User does not exist")
    if request.method == "POST":
        data = request.POST
        full_name = data.get("full_name")
        email = data.get("email")
        username = data.get("username")
        birth_date = data.get("birth_date")
        image = request.FILES.get("image")
        if full_name:
            user.full_name = full_name
        if email:
            user.email = email
        if birth_date:
            try:
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
                user.birth_date = birth_date
            except ValueError:
                return JsonResponse({"error": "Invalid date format. Expected format: 'YYYY-MM-DD'."})
        if username:
            user.username = username
        if image:
            user.image = image
        user.save()
        return JsonResponse({"success": "Profile updated successfully"})
    return render(request, "edit.html", {"user": user})
def show(request,username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "User does not exist")
    return render(request,"show.html",{"user":user})
def delete(request,username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "User does not exist")
    if user == request.user:
        return HttpResponseForbidden("You cannot delete yourself")
    user.delete()
    return HttpResponseRedirect(reverse("adminmanager"))
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Task

def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "todoApp/index.html", {
            "tasks": request.user.tasks.all()
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "todoApp/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "todoApp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "todoApp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "todoApp/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "todoApp/register.html")

@csrf_exempt
def addTask(request):
    current_user = request.user

    if (request.method == "POST"):
        task = Task(user = current_user, description = request.POST["task"])
        task.save()
        current_user.save()

    return HttpResponseRedirect(reverse("index"))
    
@csrf_exempt
def delete(request):
    data = json.loads(request.body)
    id = data.get('id')
    task = Task.objects.get(pk = id)
    task.delete()
    return HttpResponseRedirect(reverse("index"))

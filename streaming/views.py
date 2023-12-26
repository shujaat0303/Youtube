from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import User,Channel,Video,Comment


# Create your views here.
def index(request):
    return render(request,"streaming/index.html")

def playVideo(request,v):
    #get video from database then send it to playVideo.html
    return render(request,"streaming/playVideo.html")

def channel(request,c):
    #get channel data from database and pass to template
    return render(request,"streaming/channel.html")

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "streaming/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request,"streaming/login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "streaming/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "streaming/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))    
    else:
        return render(request,"streaming/signup.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

@login_required
def settings(request):
    return render(request,"streaming/settings.html")
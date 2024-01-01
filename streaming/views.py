from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import User,Channel,Video,Comment


# Create your views here.
def index(request):
    videos=Video.objects.all()
    return render(request,"streaming/index.html",{
        "videos":videos
    })

def playVideo(request,v):
    #get video from database then send it to playVideo.html
    video=Video.objects.get(id=v)
    recommendations = Video.objects.exclude(id=v)
    return render(request,"streaming/playVideo.html",{
        "video":video,
        "recommendations":recommendations
    })

@login_required
def uploadVideo(request,v):
    #get video from database then send it to playVideo.html
    # take thumbnail, video and data and add to data base and redirect user to video 
    return render(request,"streaming/uploadVideo.html")


def channel(request,c):
    #get channel data from database and pass to template
    channel=Channel.objects.get(id=c)
    if channel:
        return render(request,"streaming/channel.html",{
            "channel" : channel
        })
    return HttpResponse("404 error")

def search(request):
    query=request.GET["search_query"]
    if query:
        channels = Channel.objects.filter(name__contains=query)
        videos = Video.objects.filter(title__contains=query)
        if channels or videos:
            return render(request,"streaming/search.html",{
                "channels":channels,
                "videos":videos
            })
    
    return render(request,"streaming/search.html",{
        "message" : "No results found\nTry different keywords or remove search filters"
    })

    return HttpResponse("TODO")

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

@login_required   
def settingsp(request):
    return render(request,"streaming/settings-p.html")

@login_required
def settingsc(request):
    return render(request,"streaming/settings-c.html")

@login_required
def upload(request):
    return render(request,"streaming/uploadVideo.html")
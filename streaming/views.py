from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import User,Channel,Video,Comment
from django import forms



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
def upload(request):
    # take thumbnail, video and data and add to data base and redirect user to video 
    return render(request,"streaming/uploadVideo.html")


def channel(request,c):
    #get channel data from database and pass to template
    channel=Channel.objects.get(id=c)
    videos = Video.objects.filter(channel=c)
    if channel:
        return render(request,"streaming/channel.html",{
            "channel" : channel,
            "videos"   : videos
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


@login_required
@require_POST
def like_video(request):
    form = LikeForm(request.POST)
    if form.is_valid():
        video_id = form.cleaned_data['video_id']
        video = Video.objects.get(pk=video_id)
        video.likes.add(request.user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
@require_POST
def subscribe_channel(request):
    form = SubscribeForm(request.POST)
    if form.is_valid():
        channel_id = form.cleaned_data['channel_id']
        channel = User.objects.get(pk=channel_id)
        channel.subscribers.add(request.user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

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


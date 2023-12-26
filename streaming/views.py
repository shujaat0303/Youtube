from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"streaming/index.html")

def playVideo(request,v):
    #get video from database then send it to playVideo.html
    return render(request,"streaming/playVideo.html")

def channel(request,c):
    #get video from database then send it to channelPage.html
    return render(request,"streaming/channel.html")

def login(request):
    return render(request,"streaming/login.html")

def signup(request):
    return render(request,"streaming/signup.html")

def settingsp(request):
    return render(request,"streaming/settings-p.html")

def settingsc(request):
    return render(request,"streaming/settings-c.html")
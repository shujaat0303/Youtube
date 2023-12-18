from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"streaming/index.html")

def playVideo(request,v):
    #get video from database then send it to playVideo.html
    return render(request,"streaming/playVideo.html")
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"streaming/index.html")

def playVideo(request):
    return render(request,"streaming/playVideo.html")
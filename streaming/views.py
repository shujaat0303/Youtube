from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import User,Channel,Video,Comment
from django import forms

# Forms
class LikeForm(forms.Form):
    video_id = forms.IntegerField()

class SubscribeForm(forms.Form):
    channel_id = forms.IntegerField()      

class VideoForm(forms.ModelForm):
    class Meta:
        model=Video
        fields =['title','description','channel','thumbnail','video']
        widgets={"title":forms.TextInput(attrs={'placeholder': 'Title'}),
                "description":forms.Textarea(attrs={"cols":6,"rows":7, "class": "u-description","placeholder":"Description"}),
                "thumbnail": forms.ClearableFileInput(attrs={'accept': 'image/*'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VideoForm, self).__init__(*args, **kwargs)

    # Pre-populate form fields with user attributes
        if user:
            self.fields['channel'].initial = user.channel


class ChannelForm(forms.ModelForm):
    class Meta:
        model=Channel
        fields = ['by','name','description','cover']
        widgets={"name":forms.TextInput(attrs={'placeholder': 'Channel Name'}),
                "description":forms.Textarea(attrs={"cols":8,"rows":10, "class": "s-des","placeholder":"Description"}),}

        

    
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
    sub_form=SubscribeForm()
    like_form=LikeForm()
    subscribed= video.channel.is_user_subscribed(request.user)
    liked = video.has_user_liked(request.user)
    return render(request,"streaming/playVideo.html",{
        "video":video,
        "recommendations":recommendations,
        "sub_form":sub_form,
        "like_form":like_form,
        "subscribed":subscribed,
        "liked" : liked
    })


@login_required
def upload(request):
    # take thumbnail, video and data and add to data base and redirect user to video 
    if request.POST:
        context=VideoForm(data=request.POST,files=request.FILES)
        if context.is_valid() and context.cleaned_data["channel"]==request.user.channel:
            context.save()
            return redirect('home')
        return render(request,"streaming/uploadVideo.html",{
            "form":context
        })
    form=VideoForm(user=request.user)
    return render(request,"streaming/uploadVideo.html",{
        "form": form
    })


def channel(request,c):
    #get channel data from database and pass to template
    channel=Channel.objects.get(id=c)
    videos = Video.objects.filter(channel=c)
    if channel:
        if request.user is not None:
            subscribed=channel.is_user_subscribed(request.user)
        return render(request,"streaming/channel.html",{
            "channel" : channel,
            "videos"   : videos,
            "subscribed":subscribed
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
    print(form.is_valid())
    if form.is_valid():
        video_id = form.cleaned_data['video_id']
        video = Video.objects.get(pk=video_id)
        if(video.has_user_liked(request.user)):
            video.likes.remove(request.user)
        else:
            video.likes.add(request.user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
@require_POST
def subscribe_channel(request):
    form = SubscribeForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        channel_id = form.cleaned_data['channel_id']
        channel = Channel.objects.get(pk=channel_id)
        if(channel.is_user_subscribed(request.user)):
            channel.subscribers.remove(request.user)
        else:
            channel.subscribers.add(request.user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required(login_url='login')
def history(request):
    return render(request,"streaming/history.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            redirect_page=request.POST["next"]
            if redirect_page:
                return HttpResponseRedirect(redirect_page)
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
    if request.POST:
        context=ChannelForm(request.POST)
        channel=Channel.objects.get(by=request.user)
        if context.is_valid():
            if channel:
                name=context.cleaned_data["name"]
                description=context.cleaned_data["description"]
                cover=context.cleaned_data["cover"]
                channel=Channel(by=request.user,name=name,description=description,cover=cover)
                channel.save()
            else:
                context.save()
            redirect('channel', c=request.user.channel.id)
        return render(request,"streaming/settings-c.html",{
            "form":context
        })
    channel = request.user.channel
    if channel:
        form=ChannelForm(initial={'by':channel.by,'name':channel.name,
                'description':channel.description,'cover':channel.cover})
    else:
        form=ChannelForm(initial={'by':request.user})
    return render(request,"streaming/settings-c.html",{
        "form":form
    })


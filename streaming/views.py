from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.urls import reverse
from .models import User,Channel,Video,Comment,WatchHistory
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

        
class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","profile_pic"]
        widgets={"username":forms.TextInput(attrs={'placeholder': 'Username'}),}
    
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["comment","on"]
        widgets={"comment":forms.TextInput(attrs={'placeholder': 'Write your comment...'}),}


# Create your views here.
def index(request):
    videos=Video.objects.all()
    return render(request,"streaming/index.html",{
        "videos":videos
    })


def playVideo(request,v):

    # get video from database then send it to playVideo.html
    video=Video.objects.get(id=v)
    # update watch history
    watch_history,created = WatchHistory.objects.get_or_create(
            by=request.user,
            on=video,
        )

    if not created:
        watch_history.save()
    recommendations = Video.objects.exclude(id=v)
    sub_form=SubscribeForm()
    like_form=LikeForm()
    comment_form=CommentForm(initial={"on":video})
    subscribed= video.channel.is_user_subscribed(request.user)
    liked = video.has_user_liked(request.user)
    comments= Comment.objects.filter(on=video).order_by('-time')
    
    return render(request,"streaming/playVideo.html",{
        "video":video,
        "recommendations":recommendations,
        "sub_form":sub_form,
        "like_form":like_form,
        "subscribed":subscribed,
        "liked" : liked,
        "comment_form":comment_form,
        "comments":comments
    })


@login_required(login_url='login')
def upload(request):
    # take thumbnail, video and data and add to data base and redirect user to video 
    channel= Channel.objects.filter(by=request.user).exists()
    if not channel:
        return redirect("settings-c")
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


@login_required(login_url='login')
@require_POST
def like_video(request):
    form = LikeForm(request.POST)
    if form.is_valid():
        video_id = form.cleaned_data['video_id']
        video = Video.objects.get(pk=video_id)
        if(video.has_user_liked(request.user)):
            video.likes.remove(request.user)
        else:
            video.likes.add(request.user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required(login_url='login')
@require_POST
def comment_video(request):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
    # Save the comment
        comment = comment_form.save(commit=False)
        comment.by = request.user
        comment.save()

        # Update num_comments in the associated video
        comment.on.num_comments = Comment.objects.filter(on=comment.on).count()
        comment.on.save()

        return JsonResponse({'success': True, 'comment_id': comment.id, 'comment_html': render_to_string('streaming/comment_partial.html', {'comment': comment})})
    else:
        return JsonResponse({'success': False, 'errors': comment_form.errors})


@login_required(login_url='login')
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
    history=WatchHistory.objects.filter(by=request.user).order_by('-time')
    return render(request,"streaming/history.html",{
        'history':history
    })


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


@login_required(login_url='login')
def settings(request):
    return render(request,"streaming/settings.html")


# views.py
@login_required(login_url='login')
def settingsp(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if 'update_user' in request.POST and user_form.is_valid():
            user_form.save()
        elif 'change_password' in request.POST and password_form.is_valid():
            password_form.save()
        else:
            return render(request, "streaming/settings-p.html", {
                "user_form": user_form,
                "password_form": password_form})

        # Update the user's session to prevent them from being logged out
        update_session_auth_hash(request, request.user)
            
        return HttpResponseRedirect(reverse("home"))
    else:
        user_form = UserForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, "streaming/settings-p.html", {
        "user_form": user_form,
        "password_form": password_form
    })


@login_required(login_url='login')
def settingsc(request):
    if request.POST:
        channel= get_object_or_404(Channel, pk=request.user.channel.id)
        context=ChannelForm(request.POST,request.FILES,instance=channel)
        if context.is_valid():
            context.save()
            return HttpResponseRedirect(reverse("channel",args=[channel.id])) 
        return render(request,"streaming/settings-c.html",{
            "form":context
        })
        
    haschannel = hasattr(request.user,"channel")  
    if haschannel:
        channel = request.user.channel
        form=ChannelForm(initial={'by':channel.by,'name':channel.name,
                'description':channel.description,'cover':channel.cover})
    else:
        form=ChannelForm(initial={'by':request.user})
    return render(request,"streaming/settings-c.html",{
        "form":form
    })


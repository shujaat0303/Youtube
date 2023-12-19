from django.urls import path

from . import views

#app_name ="streaming"
urlpatterns=[
    path("",views.index,name="home"),
    path("watch/<int:v>",views.playVideo,name="playVideo"),
    path("channel/<int:c>",views.channelPage,name="channelPage")
]
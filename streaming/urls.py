from django.urls import path

from . import views

#app_name ="streaming"
urlpatterns=[
    path("",views.index,name="home"),
    path("",views.playVideo,name="playVideo")
]
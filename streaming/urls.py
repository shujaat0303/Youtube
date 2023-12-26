from django.urls import path

from . import views

#app_name ="streaming"
urlpatterns=[
    path("",views.index,name="home"),
    path("watch/<int:v>",views.playVideo,name="playVideo"),
    path("channel/<int:c>",views.channel,name="channel"),
    path("login/",views.login,name="login"),
    path("signup/",views.signup,name="signup"),
    path("settings-p/",views.settingsp,name="settings-p"),
    path("settings-c/",views.settingsc,name="settings-c")
]
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

#app_name ="streaming"
urlpatterns=[
    path("",views.index,name="home"),
    path("watch/<int:v>",views.playVideo,name="playVideo"),
    path("channel/<int:c>",views.channel,name="channel"),
    path("login/",views.login,name="login"),
    path("signup/",views.signup,name="signup"),
    path("settings/",views.settings,name="settings")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
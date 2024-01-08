from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

#app_name ="streaming"
urlpatterns=[
    path("",views.index,name="home"),
    path("watch/<int:v>",views.playVideo,name="playVideo"),
    path("channel/<int:c>",views.channel,name="channel"),
    path("login/",views.login_view,name="login"),
    path("signup/",views.signup_view,name="signup"),
    path("logout/",views.logout_view,name="logout"),
    path("settings-p/",views.settingsp,name="settings-p"),
    path("settings-c/",views.settingsc,name="settings-c"),
    path("upload/",views.upload,name="upload"),
    path("results/",views.search, name='search'),
    path("subscribe_channel/",views.subscribe_channel,name="subscribe"),
    path("like_channel/",views.like_video,name="like"),#why not like_video
    path("history/",views.history,name="history"),
    path("comment_video/",views.comment_video,name="comment")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.core.mail import send_mail
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name="eventmanager"

urlpatterns=[
    path("",homeView,name="home"),
    path("login/",login,name="login"),
    path("signup/",signup,name="signup"),
    path("dashboard/<str:user_email>",dashboard,name="dashboard"),
    path("sendMail/",sendMail,name="sendmail"),
    path("updateprofile/<str:user_email>/",updateProfile,name="updateprofile"),
    path("uploadevent/<str:user_email>/",uploadEvent,name="uploadevent"),
    path("deleteevent/",deletePost,name="deleteevent"),
    path("updateevent/",updatePost,name="updateevent"),
    path("bookevent/",bookEvent,name="bookevent"),
    path("testmail/",testMail,name="testmail"),
    path("deletemessage/",deleteMessage),
    path("getcategories/",getCategories),
    path("getsubcategories/",getSubCategories),
    path("geteventimage/",getEventImage),
]
from django.urls import path,include
from mainapp.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user',UserViewSet)
router.register(r'history',HistoryViewSet)

urlpatterns = [
    path('',home,name="home"),
    path('history/',history,name="history"),
    path('login/',login,name="login"),
    path('signup/',signup,name="signup"),
    path('sendopt/',send_otp,name='sendotp'),
    path('logout/',logout,name='logout'),
    path("api/v1/",include(router.urls))
]
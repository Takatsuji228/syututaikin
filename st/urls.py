from django.urls import path
from . import views

"""
http://localhost:8000/st/
"""

urlpatterns = [
    path('login',views.Login,name='Login'),
    path("logout",views.Logout,name="Logout"),
    path('register',views.AccountRegistration.as_view(), name='register'),
    path("home",views.home,name="home"),
    #path("home/<int:pk>",views.home,name="home"),
    path("update",views.update,name="update"),
    path("user",views.UserView,name="user"),
    path("user2",views.ListView,name="user2"),
    path("mac",views.MacView,name="mac"),
    path("mac2",views.Mac2View,name="mac"),
    path("mac3",views.Mac3View,name="mac"),
    path("wai",views.waiView,name="wai"),
    path("wai2",views.wai2View,name="wai2"),
    path("syututaikin",views.Syututaikin,name="syututaikin"),
]
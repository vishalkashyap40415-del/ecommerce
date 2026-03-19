from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('newuser/', views.newuser, name='newuser'),
    path('signup/', views.signup_page, name='signup'),
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('profile/', views.Profile, name='Profile'),
    path('myorders/', views.MyOrders, name='MyOrders'),
    path('changepassword/', views.ChangePassword, name='ChangePassword'),
]

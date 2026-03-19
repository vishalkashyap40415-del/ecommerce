from .import views
from django.urls import path

urlpatterns = [
    path('', views.HOME_Main_Page, name='Startpage'),
    path('home/', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('newuser/', views.newuser, name='newuser'),
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('signup/', views.signup_page, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('changepassword/', views.ChangePassword, name='ChangePassword'),
   

]

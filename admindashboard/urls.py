from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('check-user/', views.check_user, name='check_user'),
    path('dashboard/', views.admin_dash, name='admin_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('manage-product/', views.manage_product, name='manage_product'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('manage_product', views.manage_product, name='manage_product'),
    path('product_delete/<int:id>', views.product_delete, name='product_delete'),
    path('product_update/<int:id>', views.product_update, name='product_update'),
]

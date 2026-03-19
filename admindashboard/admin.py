from django.contrib import admin

from userdashboard.models import signup
from .models import admin_user, order, product


@admin.register(admin_user)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pname', 'pprice', 'ptype')
    search_fields = ('pname', 'ptype')


admin.site.register(order)
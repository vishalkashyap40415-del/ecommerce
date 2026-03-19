from django.contrib import admin
from .models import admin_user, product


@admin.register(admin_user)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pname', 'pprice', 'ptype')
    search_fields = ('pname', 'ptype')

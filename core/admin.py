from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Order, ContactMessage


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'phone', 'role', 'date_joined']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'phone']
    fieldsets = UserAdmin.fieldsets + (
        ('Қосымша маълыўмат', {'fields': ('phone', 'role', 'address')}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title_kk', 'category', 'price', 'power_kw', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['title_kk']
    list_editable = ['is_active', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__phone']
    list_editable = ['status']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_read', 'created_at']
    list_filter = ['is_read']
    list_editable = ['is_read']

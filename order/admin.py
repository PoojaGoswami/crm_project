from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'title', 'value', 'discount', 'final_value', 'is_paid']
    list_select_related = ['user']
    list_filter = ['date', 'user', 'title', 'value', 'discount', 'final_value', 'is_paid']
    search_fields = ['title']
    list_per_page = 50
    fields = ['date', 'user', 'title', 'value', 'discount', 'final_value', 'is_paid']
    readonly_fields = ['tag_final_value']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'qty', 'price', 'discount_price', 'final_price', 'total_price']
    list_select_related = ['product']
    list_filter = ['product', 'order', 'qty', 'price', 'discount_price', 'final_price', 'total_price']
    search_fields = ['title']
    list_per_page = 50
    fields = ['product', 'order', 'qty', 'price', 'discount_price', 'final_price', 'total_price']
    # readonly_fields = ['order']

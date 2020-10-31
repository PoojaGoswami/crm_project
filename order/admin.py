from django.contrib import admin

# Register your models here.
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['date', 'title', 'value', 'discount', 'final_value', 'is_paid']

    list_filter = ['date', 'title', 'value', 'discount', 'final_value', 'is_paid']
    search_fields = ['title']
    list_per_page = 50
    fields = ['date', 'title', 'value', 'discount', 'final_value', 'is_paid']
    readonly_fields = ['tag_final_value']

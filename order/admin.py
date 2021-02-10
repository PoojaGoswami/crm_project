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
    actions = ['download_csv']

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from io import StringIO

        # f = StringIO.StringIO()
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(['date', 'user', 'title', 'value', 'discount', 'final_value', 'is_paid'])

        for s in queryset:
            writer.writerow([s.date, s.user, s.title, s.value, s.discount, s.final_value, s.is_paid])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'qty', 'price', 'discount_price', 'final_price', 'total_price']
    list_select_related = ['product']
    list_filter = ['product', 'order', 'qty', 'price', 'discount_price', 'final_price', 'total_price']
    search_fields = ['title']
    list_per_page = 50
    fields = ['product', 'order', 'qty', 'price', 'discount_price', 'final_price', 'total_price']
    # readonly_fields = ['order']
    actions = ['download_csv']

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from io import StringIO

        # f = StringIO.StringIO()
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(['product', 'order', 'qty', 'price', 'discount_price', 'final_price', 'total_price'])

        for s in queryset:
            writer.writerow([s.product, s.order, s.qty, s.price, s.discount_price, s.final_price, s.total_price])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response




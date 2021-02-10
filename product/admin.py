from django.contrib import admin

# Register your models here.
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'flavour', 'tag_final_value', 'qty', 'active']
    list_select_related = ['category']
    list_filter = ['active', 'category']
    search_fields = ['title']
    list_per_page = 50
    fields = ['active', 'title', 'category', 'flavour', 'qty', 'value', 'discount_value', 'tag_final_value']
    autocomplete_fields = ['category']
    readonly_fields = ['tag_final_value']
    actions = ['download_csv']

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from io import StringIO

        # f = StringIO.StringIO()
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(['title', 'category', 'flavour', 'value', 'qty', 'active'])

        for s in queryset:
            writer.writerow([s.title, s.category, s.flavour, s.value, s.qty, s.active])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response

from django.contrib import admin

# Register your models here.
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['athlete_code', 'mobile', 'birth_date']
    list_select_related = ['athlete_code', 'mobile', 'birth_date']
    list_filter = ['athlete_code', 'mobile', 'birth_date']
    search_fields = ['athlete_code', 'mobile', 'birth_date']
    list_per_page = 50
    fields = ['athlete_code', 'mobile', 'birth_date']
    autocomplete_fields = ['user_id']
    # readonly_fields = ['tag_final_value']
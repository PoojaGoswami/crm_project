from django.contrib import admin

# Register your models here.
from .models import Profile, Athlete


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'athlete_code', 'mobile', 'birth_date']
    list_select_related = ['user']
    # list_select_related = ['athlete_code', 'mobile', 'birth_date']
    list_filter = ['athlete_code', 'mobile', 'birth_date']
    search_fields = ['athlete_code', 'mobile', 'birth_date']
    list_per_page = 50
    fields = ['user', 'email', 'athlete_code', 'mobile', 'address', 'birth_date']
    autocomplete_fields = ['user_id']
    # readonly_fields = ['tag_final_value']


# admin.site.register(Athlete)
@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ['email', 'athlete_code']
    list_filter = ['email', 'athlete_code']
    search_fields = ['email', 'athlete_code']
    list_per_page = 50
    fields = ['email', 'athlete_code']
    # autocomplete_fields = ['email']

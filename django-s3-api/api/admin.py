from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','age', 'email', 'image']
    search_fields = ['name', 'email']
    list_filter = ['age', 'gender']

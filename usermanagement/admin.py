from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id", "username", "email", "first_name", "last_name", "phone_no", "point"
    ]
    fields = [
         "username", "email", "first_name", "last_name", "phone_no", "point"
    ]
    search_fields = [
        "id", "username", "email", "first_name", "last_name"
    ]
    list_display_links = ["id", "username"]


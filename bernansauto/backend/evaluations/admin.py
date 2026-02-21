from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "application_type", "car", "motorcycle", "created_at")
    list_filter = ("application_type", "created_at")
    search_fields = ("name", "phone", "email", "message")
    raw_id_fields = ("car", "motorcycle")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"

from django.contrib import admin
from .models import CarApplication, MotoApplication


@admin.register(CarApplication)
class CarApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "application_type", "car", "created_at")
    list_filter = ("application_type", "created_at")
    search_fields = ("name", "phone", "email", "message")
    raw_id_fields = ("car",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"


@admin.register(MotoApplication)
class MotoApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "application_type", "motorcycle", "created_at")
    list_filter = ("application_type", "created_at")
    search_fields = ("name", "phone", "email", "message")
    raw_id_fields = ("motorcycle",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"

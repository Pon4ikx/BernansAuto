from django.contrib import admin
from .models import Car, Motorcycle, Car_Photo, Moto_Photo, Favorite


class Car_PhotoInline(admin.TabularInline):
    model = Car_Photo
    extra = 0
    fields = ("car", "link")


class Moto_PhotoInline(admin.TabularInline):
    model = Moto_Photo
    extra = 0
    fields = ("motorcycle", "link")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "marka",
        "car_model",
        "year",
        "mileage",
        "price_byn",
        "price_usd",
        "available",
        "created_at",
    )
    list_filter = ("available", "marka", "year")
    search_fields = ("marka", "car_model", "description")
    list_editable = ("available",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [Car_PhotoInline]
    fieldsets = (
        (None, {"fields": ("marka", "car_model", "year", "mileage", "description", "available")}),
        ("Двигатель и ходовая", {"fields": ("body_type", "engine_type", "transmission", "drive_type")}),
        ("Цены", {"fields": ("price_byn", "price_usd")}),
        ("Даты", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Motorcycle)
class MotorcycleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "marka",
        "moto_model",
        "year",
        "mileage",
        "engine_volume",
        "moto_type",
        "price_byn",
        "price_usd",
        "available",
        "created_at",
    )
    list_filter = ("available", "marka", "year", "moto_type")
    search_fields = ("marka", "moto_model", "description")
    list_editable = ("available",)
    readonly_fields = ("created_at",)
    inlines = [Moto_PhotoInline]
    fieldsets = (
        (None, {"fields": ("marka", "moto_model", "year", "mileage", "engine_volume", "moto_type", "description", "available")}),
        ("Цены", {"fields": ("price_byn", "price_usd")}),
        ("Даты", {"fields": ("created_at",)}),
    )


@admin.register(Car_Photo)
class Car_PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "car", "link")
    list_filter = ("car",)
    search_fields = ("car__marka", "car__car_model", "link")
    raw_id_fields = ("car",)


@admin.register(Moto_Photo)
class Moto_PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "motorcycle", "link")
    list_filter = ("motorcycle",)
    search_fields = ("motorcycle__marka", "motorcycle__moto_model", "link")
    raw_id_fields = ("motorcycle",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "car", "motorcycle", "created_at")
    list_filter = ("user",)
    search_fields = ("user__username", "car__marka", "motorcycle__marka")
    raw_id_fields = ("user", "car", "motorcycle")
    readonly_fields = ("created_at",)

from django.contrib import admin
from django.utils.html import format_html
from .models import Car, Motorcycle, Car_Photo, Moto_Photo, Favorite



class Moto_PhotoInline(admin.TabularInline):
    model = Moto_Photo
    extra = 0
    fields = ("photo",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "marka",
        "car_model",
        "year",
        "mileage",
        "engine_volume",
        "color",
        "price_byn",
        "price_usd",
        "available",
        "created_at",
    )
    list_filter = ("available", "marka", "year")
    search_fields = ("marka", "car_model", "description")
    list_editable = ("available",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("marka", "car_model", "year", "mileage", "color", "description", "available")}),
        ("Двигатель и ходовая", {"fields": ("body_type", "engine_type", "engine_volume", "transmission", "drive_type")}),
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
    list_display = ("car", "photo_thumb", "photo")
    list_filter = ("car",)
    search_fields = ("car__marka", "car__car_model")
    raw_id_fields = ("car",)
    readonly_fields = ("photo_thumb",)

    def photo_thumb(self, obj):
        if obj.pk and obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px; object-fit: contain;" />',
                obj.photo.url,
            )
        return "—"
    photo_thumb.short_description = "Превью"

    def get_fieldsets(self, request, obj=None):
        if obj and obj.photo:
            return [(None, {"fields": ("car", "photo_thumb", "photo")})]
        return [(None, {"fields": ("car", "photo")})]


@admin.register(Moto_Photo)
class Moto_PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "motorcycle", "photo_thumb", "photo")
    list_filter = ("motorcycle",)
    search_fields = ("motorcycle__marka", "motorcycle__moto_model")
    raw_id_fields = ("motorcycle",)
    readonly_fields = ("photo_thumb",)

    def photo_thumb(self, obj):
        if obj.pk and obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px; object-fit: contain;" />',
                obj.photo.url,
            )
        return "—"
    photo_thumb.short_description = "Превью"

    def get_fieldsets(self, request, obj=None):
        if obj and obj.photo:
            return [(None, {"fields": ("motorcycle", "photo_thumb", "photo")})]
        return [(None, {"fields": ("motorcycle", "photo")})]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "car", "motorcycle", "created_at")
    list_filter = ("user",)
    search_fields = ("user__username", "car__marka", "motorcycle__marka")
    raw_id_fields = ("user", "car", "motorcycle")
    readonly_fields = ("created_at",)

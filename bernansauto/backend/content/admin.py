from django.contrib import admin
from .models import Contact, News


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "address", "phone", "email", "work_hours")
    search_fields = ("address", "phone", "email")


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published_at")
    list_filter = ("published_at",)
    search_fields = ("title", "text")
    date_hierarchy = "published_at"

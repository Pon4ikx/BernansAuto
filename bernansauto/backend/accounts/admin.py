from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from .models import User

# Register your models here.
admin.site.site_header = "BernansAuto"  # Заголовок панели администратора
admin.site.site_title = "Администрирование BernansAuto"  # Заголовок на вкладке браузера
admin.site.index_title = "Администрирование"  # Текст на главной странице админки
admin.site.site_url = settings.FRONTEND_BASE_URL


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'username', 'email', 'phone', 'date_registered', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    # date_registered создаётся автоматически (auto_now_add), поэтому в форме делаем его только для чтения
    readonly_fields = ('date_registered',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'date_registered')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2', 'is_active','is_staff', 'is_superuser')}
         ),
    )

    search_fields = ('username', 'email', 'phone')
    ordering = ('id',)


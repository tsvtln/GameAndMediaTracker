from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import AppUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('avatar', 'favorites_count', 'saves_count', 'screenshots_count')
    readonly_fields = ('favorites_count', 'saves_count', 'screenshots_count', 'created_at', 'updated_at')


@admin.register(AppUser)
class AppUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'favorites_count', 'saves_count', 'screenshots_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Profile Information'), {'fields': ('avatar',)}),
        (_('Statistics'), {'fields': ('favorites_count', 'saves_count', 'screenshots_count')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )


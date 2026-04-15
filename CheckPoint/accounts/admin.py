from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as gtl
from CheckPoint.accounts.models import AppUser, Profile, Screenshot, FavoriteScreenshot


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
        (gtl('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (gtl('Important dates'), {'fields': ('last_login', 'date_joined')}),
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
        (gtl('User'), {'fields': ('user',)}),
        (gtl('Profile Information'), {'fields': ('avatar',)}),
        (gtl('Statistics'), {'fields': ('favorites_count', 'saves_count', 'screenshots_count')}),
        (gtl('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ('game_name', 'platform', 'uploaded_by', 'likes', 'created_at')
    list_filter = ('platform', 'created_at')
    search_fields = ('game_name', 'uploaded_by__username')
    readonly_fields = ('likes', 'created_at')
    ordering = ('-created_at',)


@admin.register(FavoriteScreenshot)
class FavoriteScreenshotAdmin(admin.ModelAdmin):
    list_display = ('user', 'screenshot', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'screenshot__game_name')
    ordering = ('-created_at',)

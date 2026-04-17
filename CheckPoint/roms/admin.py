from django.contrib import admin
from CheckPoint.roms.models import Rom, Comment, Review, FavoriteRom, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Rom)
class RomAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'genre', 'uploaded_by', 'downloads', 'rating', 'created_at')
    list_filter = ('platform', 'genre', 'created_at')
    search_fields = ('title', 'description', 'uploaded_by__username')
    readonly_fields = ('downloads', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)

    fieldsets = (
        ('Game Information', {
            'fields': ('title', 'platform', 'genre', 'description', 'tags')
        }),
        ('Files', {
            'fields': ('rom_file', 'box_art')
        }),
        ('Statistics', {
            'fields': ('uploaded_by', 'downloads', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(FavoriteRom)
class FavoriteRomAdmin(admin.ModelAdmin):
    list_display = ('user', 'rom', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'rom__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'rom', 'text_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'rom__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def text_preview(self, obj):
        return obj.text[:200] + '...' if len(obj.text) > 200 else obj.text
    text_preview.short_description = 'Comment'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rom', 'rating', 'text_preview', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('text', 'user__username', 'rom__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def text_preview(self, obj):
        return obj.text
    text_preview.short_description = 'Review'



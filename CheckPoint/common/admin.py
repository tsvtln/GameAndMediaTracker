from django.contrib import admin
from CheckPoint.common.models import Event, Board, Thread, Post


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'platform', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'platform', 'event_date')
    search_fields = ('title', 'description', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('event_date',)

    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'event_date', 'platform', 'description')
        }),

        ('Status', {
            'fields': ('status', 'created_by')
        }),

        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'author', 'is_pinned', 'is_locked', 'created_at')
    list_filter = ('board', 'is_pinned', 'is_locked', 'created_at')
    search_fields = ('title', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-is_pinned', '-created_at')

    fieldsets = (
        ('Thread Information', {
            'fields': ('board', 'title', 'slug', 'author')
        }),

        ('Settings', {
            'fields': ('is_pinned', 'is_locked')
        }),

        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')
    list_filter = ('created_at', 'thread__board')
    search_fields = ('content', 'author__username', 'thread__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Post Information', {
            'fields': ('thread', 'author', 'content')
        }),

        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

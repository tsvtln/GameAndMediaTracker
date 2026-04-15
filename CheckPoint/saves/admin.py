from django.contrib import admin
from CheckPoint.saves.models import Save, SaveVote


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    list_display = ('game_title', 'platform', 'save_type', 'progress', 'completion', 'uploaded_by', 'downloads', 'rating', 'created_at')
    list_filter = ('platform', 'save_type', 'progress', 'created_at')
    search_fields = ('game_title', 'description', 'uploaded_by__username')
    readonly_fields = ('downloads', 'upvotes', 'downvotes', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(SaveVote)
class SaveVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'save_file', 'vote_type', 'created_at')
    list_filter = ('vote_type', 'created_at')
    search_fields = ('user__username', 'save_file__game_title')
    ordering = ('-created_at',)


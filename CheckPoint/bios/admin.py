from django.contrib import admin
from CheckPoint.bios.models import Bios


@admin.register(Bios)
class BiosAdmin(admin.ModelAdmin):
    list_display = ('platform', 'bios_file', 'uploaded_by', 'downloads', 'created_at')
    list_filter = ('platform', 'source', 'created_at')
    search_fields = ('platform', 'description', 'uploaded_by__username')
    readonly_fields = ('downloads', 'created_at', 'updated_at')
    ordering = ('-created_at',)

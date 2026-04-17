from celery import shared_task
from django.db.models import F
from CheckPoint.roms.models import Rom


@shared_task
def recalculate_rom_rating(rom_id):
    try:
        rom = Rom.objects.get(pk=rom_id)
    except Rom.DoesNotExist:
        return {'status': 'missing', 'rom_id': rom_id}

    rom.update_rating()
    return {'status': 'ok', 'rom_id': rom_id, 'rating': float(rom.rating)}


@shared_task
def increment_rom_downloads(rom_id):
    updated = Rom.objects.filter(pk=rom_id).update(downloads=F('downloads') + 1)
    return {'status': 'ok' if updated else 'missing', 'rom_id': rom_id}

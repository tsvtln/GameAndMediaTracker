from celery import shared_task
from django.db.models import F
from CheckPoint.bios.models import Bios


@shared_task
def increment_bios_downloads(bios_id):
    updated = Bios.objects.filter(pk=bios_id).update(downloads=F('downloads') + 1)
    return {'status': 'ok' if updated else 'missing', 'bios_id': bios_id}

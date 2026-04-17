from celery import shared_task
from django.db.models import F
from CheckPoint.saves.models import Save


@shared_task
def increment_save_downloads(save_id):
    updated = Save.objects.filter(pk=save_id).update(downloads=F('downloads') + 1)
    return {'status': 'ok' if updated else 'missing', 'save_id': save_id}


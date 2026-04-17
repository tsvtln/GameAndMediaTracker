from celery import shared_task
from django.db.models import Count
from CheckPoint.accounts.models import Screenshot, FavoriteScreenshot, Profile


@shared_task
def sync_screenshot_favorite_counters(screenshot_id, user_id):
    from CheckPoint.roms.models import FavoriteRom

    likes_count = FavoriteScreenshot.objects.filter(screenshot_id=screenshot_id).count()
    Screenshot.objects.filter(pk=screenshot_id).update(likes=likes_count)

    screenshot_favorites = FavoriteScreenshot.objects.filter(user_id=user_id).count()
    rom_favorites = FavoriteRom.objects.filter(user_id=user_id).count()
    Profile.objects.filter(user_id=user_id).update(favorites_count=screenshot_favorites + rom_favorites)

    return {
        'status': 'ok',
        'screenshot_id': screenshot_id,
        'user_id': user_id,
        'likes_count': likes_count,
        'favorites_count': screenshot_favorites + rom_favorites,
    }


@shared_task
def check_profile_counters():
    from CheckPoint.roms.models import FavoriteRom
    from CheckPoint.saves.models import Save

    screenshot_fav_counts = {
        item['user_id']: item['total']
        for item in FavoriteScreenshot.objects.values('user_id').annotate(total=Count('id'))
    }
    rom_fav_counts = {
        item['user_id']: item['total']
        for item in FavoriteRom.objects.values('user_id').annotate(total=Count('id'))
    }
    save_counts = {
        item['uploaded_by_id']: item['total']
        for item in Save.objects.values('uploaded_by_id').annotate(total=Count('id'))
    }
    screenshot_counts = {
        item['uploaded_by_id']: item['total']
        for item in Screenshot.objects.values('uploaded_by_id').annotate(total=Count('id'))
    }

    checked = 0
    updated = 0

    for profile in Profile.objects.all():
        checked += 1
        user_id = profile.user_id

        favorites_count = screenshot_fav_counts.get(user_id, 0) + rom_fav_counts.get(user_id, 0)
        saves_count = save_counts.get(user_id, 0)
        screenshots_count = screenshot_counts.get(user_id, 0)

        update_fields = {}
        if profile.favorites_count != favorites_count:
            update_fields['favorites_count'] = favorites_count
        if profile.saves_count != saves_count:
            update_fields['saves_count'] = saves_count
        if profile.screenshots_count != screenshots_count:
            update_fields['screenshots_count'] = screenshots_count

        if update_fields:
            Profile.objects.filter(pk=profile.pk).update(**update_fields)
            updated += 1

    return {
        'status': 'ok',
        'profiles_checked': checked,
        'profiles_updated': updated,
    }

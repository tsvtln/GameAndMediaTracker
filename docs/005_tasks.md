# CheckPoint - Async Tasks (Celery)

## Overview

CheckPoint uses **Celery** with **Redis** as the message broker to handle operations that should not block HTTP requests.  
This includes download counter increments, rating recalculations, and profile statistics syncing.

A **Celery Beat** periodic task also runs every hour to audit all profile counters and correct any drifts.

---

## Setup

Celery is configured in `CheckPoint/celery.py`:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CheckPoint.settings')
app = Celery('CheckPoint')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

Relevant settings in `settings.py`:

```python
CELERY_BROKER_URL = config('CELERY_BROKER_URL')   # e.g. redis://localhost:6379/0
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

To start the worker:
```sh
celery -A CheckPoint worker --loglevel=info
```

To start the beat scheduler:
```sh
celery -A CheckPoint beat --loglevel=info
```

---

## Tasks

### `accounts` app - `CheckPoint/accounts/tasks.py`

---

#### `sync_screenshot_favorite_counters(screenshot_id, user_id)`

**Triggered by**: `toggle_favorite_screenshot` view, via `.delay()` after a favorite/unfavorite action.

**What it does**:
1. Counts all `FavoriteScreenshot` entries for the screenshot → updates `Screenshot.likes`.
2. Counts all `FavoriteScreenshot` + `FavoriteRom` entries for the user → updates `Profile.favorites_count`.

```python
@shared_task
def sync_screenshot_favorite_counters(screenshot_id, user_id):
    likes_count = FavoriteScreenshot.objects.filter(screenshot_id=screenshot_id).count()
    Screenshot.objects.filter(pk=screenshot_id).update(likes=likes_count)

    screenshot_favorites = FavoriteScreenshot.objects.filter(user_id=user_id).count()
    rom_favorites = FavoriteRom.objects.filter(user_id=user_id).count()
    Profile.objects.filter(user_id=user_id).update(favorites_count=screenshot_favorites + rom_favorites)
```

**Return example**:
```json
{
  "status": "ok",
  "screenshot_id": 42,
  "user_id": 7,
  "likes_count": 5,
  "favorites_count": 12
}
```

---

#### `check_profile_counters()`

**Triggered by**: Celery Beat - runs **every hour** (`crontab(minute=0)`).

**What it does**:  
Performs a full audit of all `Profile` records, comparing stored counter values against actual DB counts.  
Only updates profiles where a mismatch is detected, minimizing unnecessary writes.

Counters checked:
- `favorites_count` (screenshot favorites + ROM favorites)
- `saves_count` (uploaded saves)
- `screenshots_count` (uploaded screenshots)

> This task acts as a safety net - signals handle real-time updates, 
but this periodic task catches any counters that fall out of sync due to edge cases (e.g. bulk deletes, admin actions).

---

### `roms` app - `CheckPoint/roms/tasks.py`

---

#### `recalculate_rom_rating(rom_id)`

**Triggered by**: Views that create/edit/delete reviews (can be called via `.delay()`).

**What it does**: Fetches the `Rom` by `rom_id` and calls `rom.update_rating()` to recalculate the aggregate rating from all reviews.

```python
@shared_task
def recalculate_rom_rating(rom_id):
    try:
        rom = Rom.objects.get(pk=rom_id)
    except Rom.DoesNotExist:
        return {'status': 'missing', 'rom_id': rom_id}

    rom.update_rating()
    return {'status': 'ok', 'rom_id': rom_id, 'rating': float(rom.rating)}
```

**Return example**:
```json
{
  "status": "ok",
  "rom_id": 5,
  "rating": 4.3
}
```

---

#### `increment_rom_downloads(rom_id)`

**Triggered by**: ROM download view, via `.delay()`.

**What it does**: Uses a direct `UPDATE` query with `F('downloads') + 1` to safely increment the download counter without a read-modify-write cycle.

```python
@shared_task
def increment_rom_downloads(rom_id):
    updated = Rom.objects.filter(pk=rom_id).update(downloads=F('downloads') + 1)
    return {'status': 'ok' if updated else 'missing', 'rom_id': rom_id}
```

---

### `saves` app - `CheckPoint/saves/tasks.py`

---

#### `increment_save_downloads(save_id)`

**Triggered by**: Save file download view, via `.delay()`.

**What it does**: Same pattern as `increment_rom_downloads` - atomic `F()` increment on `Save.downloads`.

```python
@shared_task
def increment_save_downloads(save_id):
    updated = Save.objects.filter(pk=save_id).update(downloads=F('downloads') + 1)
    return {'status': 'ok' if updated else 'missing', 'save_id': save_id}
```

---

## Periodic Tasks (Beat Schedule)

Configured in `settings.py`:

```python
CELERY_BEAT_SCHEDULE = {
    'check-profile-counters-hourly': {
        'task': 'CheckPoint.accounts.tasks.check_profile_counters',
        'schedule': crontab(minute=0),  # runs at the top of every hour
    },
}
```

The schedule is also manageable via the **Django admin** panel thanks to the `django-celery-beat` integration.

---

## Task Summary

| Task                                | App      | Trigger                        | Purpose                                               |
|-------------------------------------|----------|--------------------------------|-------------------------------------------------------|
| `sync_screenshot_favorite_counters` | accounts | Screenshot favorite/unfavorite | Sync `Screenshot.likes` and `Profile.favorites_count` |
| `check_profile_counters`            | accounts | Periodic (hourly)              | Audit & repair all profile statistic counters         |
| `recalculate_rom_rating`            | roms     | Review create/edit/delete      | Recalculate `Rom.rating` from all reviews             |
| `increment_rom_downloads`           | roms     | ROM download                   | Atomically increment `Rom.downloads`                  |
| `increment_save_downloads`          | saves    | Save download                  | Atomically increment `Save.downloads`                 |

---

#### Next Page: [Project Setup](001_project_setup.md)

---

<div style="display: flex">
  <a href="../README.md">
    <svg width="20" height="20" fill="blue" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" version="1.1" id="Capa_1" width="800px" height="800px" viewBox="0 0 495.398 495.398" xml:space="preserve">
    <g>
        <g>
            <g>
                <path d="M487.083,225.514l-75.08-75.08V63.704c0-15.682-12.708-28.391-28.413-28.391c-15.669,0-28.377,12.709-28.377,28.391     v29.941L299.31,37.74c-27.639-27.624-75.694-27.575-103.27,0.05L8.312,225.514c-11.082,11.104-11.082,29.071,0,40.158     c11.087,11.101,29.089,11.101,40.172,0l187.71-187.729c6.115-6.083,16.893-6.083,22.976-0.018l187.742,187.747     c5.567,5.551,12.825,8.312,20.081,8.312c7.271,0,14.541-2.764,20.091-8.312C498.17,254.586,498.17,236.619,487.083,225.514z"/>
                <path d="M257.561,131.836c-5.454-5.451-14.285-5.451-19.723,0L72.712,296.913c-2.607,2.606-4.085,6.164-4.085,9.877v120.401     c0,28.253,22.908,51.16,51.16,51.16h81.754v-126.61h92.299v126.61h81.755c28.251,0,51.159-22.907,51.159-51.159V306.79     c0-3.713-1.465-7.271-4.085-9.877L257.561,131.836z"/>
            </g>
        </g>
    </g>
    </svg>
  </a>
 <a style="margin-left: 10px" href="../README.md">Home</a>
</div>

---


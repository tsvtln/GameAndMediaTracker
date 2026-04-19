# CheckPoint - Django Signals

## Overview

Signals are used throughout the project to keep related data in sync automatically, without polluting views or models with cross-app logic.  
All signals follow Django's `post_save` / `post_delete` pattern.

---

## `accounts` app signals

**File**: `CheckPoint/accounts/signals.py`

---

### `create_user_profile`

**Trigger**: `post_save` on `AppUser`, only when `created=True` (i.e. new user).

**What it does**:
1. Creates a `Profile` instance linked to the new `AppUser`.
2. Attempts to add the user to the **Regular Users** group.  
   If the group does not exist yet (e.g. before running `create_user_groups`), it silently skips the assignment.

```python
@receiver(post_save, sender=AppUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        try:
            regular_users_group = Group.objects.get(name='Regular Users')
            instance.groups.add(regular_users_group)
        except Group.DoesNotExist:
            pass
```

---

### `save_user_profile`

**Trigger**: `post_save` on `AppUser` (every save, not just creation).

**What it does**: Saves the linked profile whenever the user object is saved, keeping the `Profile.updated_at` field current.

```python
@receiver(post_save, sender=AppUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

---

### `decrement_screenshot_count_on_delete`

**Trigger**: `post_delete` on `Screenshot`.

**What it does**: Calls `profile.decrement_screenshots()` on the uploader's profile when a screenshot is deleted, 
keeping `Profile.screenshots_count` accurate without a full recount.

```python
@receiver(post_delete, sender=Screenshot)
def decrement_screenshot_count_on_delete(sender, instance, **kwargs):
    if instance.uploaded_by and hasattr(instance.uploaded_by, 'profile'):
        instance.uploaded_by.profile.decrement_screenshots()
```

---

## `roms` app signals

**File**: `CheckPoint/roms/signals.py`

---

### `update_rom_rating_on_review_save`

**Trigger**: `post_save` on `Review`.

**What it does**: Calls `rom.update_rating()` every time a review is created or edited, keeping the ROM's cached aggregate `rating` field up to date.

```python
@receiver(post_save, sender=Review)
def update_rom_rating_on_review_save(sender, instance, **kwargs):
    instance.rom.update_rating()
```

---

### `update_rom_rating_on_review_delete`

**Trigger**: `post_delete` on `Review`.

**What it does**: Same as above, recalculates the rating when a review is removed.

```python
@receiver(post_delete, sender=Review)
def update_rom_rating_on_review_delete(sender, instance, **kwargs):
    instance.rom.update_rating()
```

> **Note**: For high-traffic scenarios, rating recalculation is also available as an async Celery task 
(`recalculate_rom_rating`). The signals provide immediate consistency; the task can be used when offloading is preferred.

---

## `saves` app signals

**File**: `CheckPoint/saves/signals.py`

---

### `increment_saves_count_on_create`

**Trigger**: `post_save` on `Save`, only on `created=True`.

**What it does**: Calls `profile.increment_saves()` on the uploader's profile when a new save file is uploaded.

```python
@receiver(post_save, sender=Save, dispatch_uid="increment_saves_count")
def increment_saves_count_on_create(sender, instance, created, **kwargs):
    if created and instance.uploaded_by and hasattr(instance.uploaded_by, 'profile'):
        instance.uploaded_by.profile.increment_saves()
```

---

### `decrement_saves_count_on_delete`

**Trigger**: `post_delete` on `Save`.

**What it does**: Calls `profile.decrement_saves()` when a save file is deleted.

```python
@receiver(post_delete, sender=Save, dispatch_uid="decrement_saves_count")
def decrement_saves_count_on_delete(sender, instance, **kwargs):
    if instance.uploaded_by and hasattr(instance.uploaded_by, 'profile'):
        instance.uploaded_by.profile.decrement_saves()
```

---

## Signal Summary

| Signal                                 | App      | Trigger                      | Effect                                       |
|----------------------------------------|----------|------------------------------|----------------------------------------------|
| `create_user_profile`                  | accounts | `AppUser` post_save (create) | Create `Profile`, assign Regular Users group |
| `save_user_profile`                    | accounts | `AppUser` post_save (any)    | Save linked `Profile`                        |
| `decrement_screenshot_count_on_delete` | accounts | `Screenshot` post_delete     | Decrement `Profile.screenshots_count`        |
| `update_rom_rating_on_review_save`     | roms     | `Review` post_save           | Recalculate `Rom.rating`                     |
| `update_rom_rating_on_review_delete`   | roms     | `Review` post_delete         | Recalculate `Rom.rating`                     |
| `increment_saves_count_on_create`      | saves    | `Save` post_save (create)    | Increment `Profile.saves_count`              |
| `decrement_saves_count_on_delete`      | saves    | `Save` post_delete           | Decrement `Profile.saves_count`              |

---

#### Next Page: [Tasks (Async / Celery)](005_tasks.md)

---

<div style="display: flex">
  <a href="../README.md">
    <svg width="20" height="20" fill="blue" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" version="1.1" id="Capa_1" width="800px" height="800px" viewBox="0 0 495.398 495.398" xml:space="preserve">
    <g>
        <g>
            <g>
                <path d="M487.083,225.514l-75.08-75.08V63.704c0-15.682-12.708-28.391-28.391-28.391c-15.669,0-28.377,12.709-28.377,28.391     v29.941L299.31,37.74c-27.639-27.624-75.694-27.575-103.27,0.05L8.312,225.514c-11.082,11.104-11.082,29.071,0,40.158     c11.087,11.101,29.089,11.101,40.172,0l187.71-187.729c6.115-6.083,16.893-6.083,22.976-0.018l187.742,187.747     c5.567,5.551,12.825,8.312,20.081,8.312c7.271,0,14.541-2.764,20.091-8.312C498.17,254.586,498.17,236.619,487.083,225.514z"/>
                <path d="M257.561,131.836c-5.454-5.451-14.285-5.451-19.723,0L72.712,296.913c-2.607,2.606-4.085,6.164-4.085,9.877v120.401     c0,28.253,22.908,51.16,51.16,51.16h81.754v-126.61h92.299v126.61h81.755c28.251,0,51.159-22.907,51.159-51.159V306.79     c0-3.713-1.465-7.271-4.085-9.877L257.561,131.836z"/>
            </g>
        </g>
    </g>
    </svg>
  </a>
 <a style="margin-left: 10px" href="../README.md">Home</a>
</div>

---


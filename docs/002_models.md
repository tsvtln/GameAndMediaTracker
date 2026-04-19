# CheckPoint - Models Documentation

## Overview

The project is split into five Django apps, each owning its relevant models.  
This page documents every model, its fields, and its key behavior.

---

## Table of Contents

- [accounts app](#accounts-app)
  - [AppUser](#appuser)
  - [Profile](#profile)
  - [Screenshot](#screenshot)
  - [FavoriteScreenshot](#favoritescreenshot)
- [roms app](#roms-app)
  - [Tag](#tag)
  - [Rom](#rom)
  - [Comment](#comment)
  - [Review](#review)
  - [ReviewLike](#reviewlike)
  - [FavoriteRom](#favoriterom)
- [bios app](#bios-app)
  - [Bios](#bios)
- [saves app](#saves-app)
  - [Save](#save)
  - [SaveVote](#savevote)
- [common app](#common-app)
  - [Event](#event)
  - [Board](#board)
  - [Thread](#thread)
  - [Post](#post)

---

## `accounts` app

### **AppUser**

Custom user model that extends Django's `AbstractUser`.  
Username is the primary authentication field; email is also required and unique.

| Field       | Type           | Description                                                     |
|-------------|----------------|-----------------------------------------------------------------|
| `username`  | `CharField`    | Unique username, max 150 chars. Primary login field.            |
| `email`     | `EmailField`   | Unique email address.                                           |
| `is_staff`  | `BooleanField` | Whether the user has access to admin features. Default `False`. |
| `is_active` | `BooleanField` | Whether the account is active. Default `True`.                  |

**Manager**: `AppUserManager` - custom manager that requires both `username` and `email` to create any user.

**Meta**: ordered by `-date_joined`.

---

### **Profile**

One-to-one extension of `AppUser` that holds avatar and activity statistics.  
Created automatically via a Django signal when a new `AppUser` is saved.

![profileExample](/docs/_assets/profile_example.png)

| Field               | Type                      | Description                                            |
|---------------------|---------------------------|--------------------------------------------------------|
| `user`              | `OneToOneField → AppUser` | The linked user account. Cascades on delete.           |
| `avatar`            | `ImageField`              | Optional profile picture. Uploads to `avatars/%Y/%m/`. |
| `favorites_count`   | `PositiveIntegerField`    | Cached total of favorited ROMs + favorite screenshots. |
| `saves_count`       | `PositiveIntegerField`    | Cached count of uploaded save files.                   |
| `screenshots_count` | `PositiveIntegerField`    | Cached count of uploaded screenshots.                  |
| `created_at`        | `DateTimeField`           | Auto-set on creation.                                  |
| `updated_at`        | `DateTimeField`           | Auto-updated on every save.                            |

**Key methods**:

| Method                                                | Purpose                                                      |
|-------------------------------------------------------|--------------------------------------------------------------|
| `increment_favorites()` / `decrement_favorites()`     | Atomically update `favorites_count` using `F()` expressions. |
| `increment_saves()` / `decrement_saves()`             | Atomically update `saves_count`.                             |
| `increment_screenshots()` / `decrement_screenshots()` | Atomically update `screenshots_count`.                       |

> All counter methods use `Model.objects.filter(pk=...).update(field=F(...))` 
followed by `refresh_from_db()` to avoid race conditions.

---

### **Screenshot**

A user-uploaded in-game screenshot.

![screenshotsExample](/docs/_assets/screenshots_example.png)

| Field         | Type                   | Description                                             |
|---------------|------------------------|---------------------------------------------------------|
| `game_name`   | `CharField`            | Name of the game the screenshot is from.                |
| `platform`    | `CharField`            | Platform choice (shared `PLATFORM_CHOICES`).            |
| `screenshot`  | `ImageField`           | Image file. Allowed: `.png .jpg .jpeg .webp`. Max 5 MB. |
| `uploaded_by` | `ForeignKey → AppUser` | The uploader. Cascades on delete.                       |
| `likes`       | `PositiveIntegerField` | Number of users who have favorited this screenshot.     |
| `created_at`  | `DateTimeField`        | Auto-set on creation.                                   |

_NOTE:_ _The `likes` field is a cached count of how many users have favorited this screenshot. It's not displayed and is 
currently used only for tracking the ranking of screenshots for the "Top Rated" page.  
It is updated asynchronously via Celery tasks whenever a user favorites or unfavorites a screenshot._

**Meta**: ordered by `-created_at`.

---

### **FavoriteScreenshot**

Through model linking a user to a screenshot they have favorited.

| Field        | Type                      | Description               |
|--------------|---------------------------|---------------------------|
| `user`       | `ForeignKey → AppUser`    | The user who favorited.   |
| `screenshot` | `ForeignKey → Screenshot` | The favorited screenshot. |
| `created_at` | `DateTimeField`           | When it was favorited.    |

**Meta**: `unique_together = ('user', 'screenshot')` - one favorite per user per screenshot.  
**Note**: Users cannot favorite their own screenshots (enforced in the view).

---

## `roms` app

![topROMsExample](/docs/_assets/top_roms.png)

### **Tag**

Simple tagging model for ROMs (e.g. `"multiplayer"`, `"classic"`, `"arcade"`).

| Field        | Type            | Description                    |
|--------------|-----------------|--------------------------------|
| `name`       | `CharField`     | Unique tag name, max 50 chars. |
| `slug`       | `SlugField`     | Unique URL-friendly slug.      |
| `created_at` | `DateTimeField` | Auto-set on creation.          |

---

### **Rom**

The central model of the ROMs app which represents a single uploadable ROM file.

| Field          | Type                        | Description                                                                        |
|----------------|-----------------------------|------------------------------------------------------------------------------------|
| `title`        | `CharField`                 | Game title, max 200 chars.                                                         |
| `platform`     | `CharField`                 | Platform choice (e.g. NES, SNES, GBA).                                             |
| `genre`        | `CharField`                 | Genre choice (e.g. RPG, Action, Sports).                                           |
| `description`  | `TextField`                 | Optional description.                                                              |
| `rom_file`     | `FileField`                 | ROM file. Allowed: `.zip .7z .rar .nes .sfc .gba .iso .smd .bin .cue`. Max 500 MB. |
| `box_art`      | `ImageField`                | Required box art image.                                                            |
| `uploaded_by`  | `ForeignKey → AppUser`      | The uploader. Cascades on delete.                                                  |
| `downloads`    | `PositiveIntegerField`      | Total download count. Default `0`.                                                 |
| `rating`       | `DecimalField`              | Aggregate rating (1 decimal place). Auto-calculated from reviews.                  |
| `tags`         | `ManyToManyField → Tag`     | Optional tags for categorisation.                                                  |
| `favorited_by` | `ManyToManyField → AppUser` | Through `FavoriteRom`.                                                             |
| `created_at`   | `DateTimeField`             | Auto-set on creation.                                                              |
| `updated_at`   | `DateTimeField`             | Auto-updated on every save.                                                        |

**Key methods**:

| Method                  | Purpose                                                               |
|-------------------------|-----------------------------------------------------------------------|
| `increment_downloads()` | Increment the download counter and save.                              |
| `update_rating()`       | Recalculate `rating` as average of all linked `Review.rating` values. |

---

### **Comment**

A free-text comment left by a user on a ROM.

| Field                       | Type                   | Description                 |
|-----------------------------|------------------------|-----------------------------|
| `rom`                       | `ForeignKey → Rom`     | The ROM being commented on. |
| `user`                      | `ForeignKey → AppUser` | Comment author.             |
| `text`                      | `TextField`            | Comment content.            |
| `created_at` / `updated_at` | `DateTimeField`        | Timestamps.                 |

**Meta**: one user can leave multiple comments. Ordered by `-created_at`.

---

### **Review**

A rated review (1–5 stars) left by a user on a ROM.  
Changing or deleting a review automatically triggers ROM rating recalculation via signals.

| Field                       | Type                        | Description           |
|-----------------------------|-----------------------------|-----------------------|
| `rom`                       | `ForeignKey → Rom`          | The reviewed ROM.     |
| `user`                      | `ForeignKey → AppUser`      | Reviewer.             |
| `rating`                    | `PositiveIntegerField`      | Star rating 1–5.      |
| `text`                      | `TextField`                 | Review text body.     |
| `liked_by`                  | `ManyToManyField → AppUser` | Through `ReviewLike`. |
| `created_at` / `updated_at` | `DateTimeField`             | Timestamps.           |

**Meta**: `unique_together = ['rom', 'user']` - one review per user per ROM.

**Property**: `likes_count` - returns the number of users who liked this review.

---

### **ReviewLike**

Through model for the many-to-many relationship between users and reviews they liked.

| Field        | Type                   | Description             |
|--------------|------------------------|-------------------------|
| `user`       | `ForeignKey → AppUser` | The user who liked.     |
| `review`     | `ForeignKey → Review`  | The liked review.       |
| `created_at` | `DateTimeField`        | When the like was made. |

**Meta**: `unique_together = ('user', 'review')`.

---

### **FavoriteRom**

Through model linking a user to a ROM they have favorited.

| Field        | Type                   | Description            |
|--------------|------------------------|------------------------|
| `user`       | `ForeignKey → AppUser` | The user.              |
| `rom`        | `ForeignKey → Rom`     | The favorited ROM.     |
| `created_at` | `DateTimeField`        | When it was favorited. |

**Meta**: `unique_together = ('user', 'rom')`.

---

## `bios` app

![biosExample](/docs/_assets/bios_example.png)

### **Bios**

Represents an uploaded BIOS file. Uploads are restricted to **Moderators** and **Verified Users**.

| Field                       | Type                   | Description                                                                                 |
|-----------------------------|------------------------|---------------------------------------------------------------------------------------------|
| `platform`                  | `CharField`            | Target platform. Extends the shared `PLATFORM_CHOICES` with MAME, FinalBurn NEO, RetroArch. |
| `bios_file`                 | `FileField`            | BIOS file. Allowed: `.bin .rom .zip .gz .pup`. Max 5 GB.                                    |
| `description`               | `TextField`            | Describes the BIOS file(s) in this upload.                                                  |
| `source`                    | `CharField`            | Upload source (choice field via `SOURCE_CHOICES`).                                          |
| `uploaded_by`               | `ForeignKey → AppUser` | The uploader. Cascades on delete.                                                           |
| `downloads`                 | `PositiveIntegerField` | Download counter. Default `0`.                                                              |
| `created_at` / `updated_at` | `DateTimeField`        | Timestamps.                                                                                 |

**Key method**: `increment_downloads()` - increments and saves the download counter.

---

## `saves` app

![savesExample](/docs/_assets/saves_example.png)

### **Save**

Represents an uploaded game save file.

| Field                       | Type                   | Description                                                              |
|-----------------------------|------------------------|--------------------------------------------------------------------------|
| `game_title`                | `CharField`            | Name of the game.                                                        |
| `platform`                  | `CharField`            | Platform (from `SAVE_PLATFORM_CHOICES`).                                 |
| `save_type`                 | `CharField`            | Type of save (from `SAVE_TYPE_CHOICES`, e.g. Quick Save, Progress Save). |
| `progress`                  | `CharField`            | Game progress stage (from `PROGRESS_CHOICES`).                           |
| `mission_detail`            | `CharField`            | Optional specific mission/checkpoint description.                        |
| `description`               | `TextField`            | Optional longer description.                                             |
| `completion`                | `PositiveIntegerField` | Completion percentage, 0–100.                                            |
| `save_file`                 | `FileField`            | Save file. Allowed: `.zip .rar .7z .sav .srm .state .dat`. Max 50 MB.    |
| `save_image`                | `ImageField`           | Optional cover/screenshot image for the save.                            |
| `uploaded_by`               | `ForeignKey → AppUser` | The uploader. Cascades on delete.                                        |
| `downloads`                 | `PositiveIntegerField` | Download counter. Default `0`.                                           |
| `upvotes`                   | `PositiveIntegerField` | Total upvote count for this save.                                        |
| `downvotes`                 | `PositiveIntegerField` | Total downvote count for this save.                                      |
| `created_at` / `updated_at` | `DateTimeField`        | Timestamps.                                                              |

**Property**: `rating` - derived score:  
`round((upvotes / total_votes) * 5, 1)` - returns 0 if no votes.

**Key method**: `increment_downloads()` - increments and saves the download counter.

---

### **SaveVote**

Tracks a single user's vote (upvote or downvote) on a save file.

| Field        | Type                   | Description                                       |
|--------------|------------------------|---------------------------------------------------|
| `save_file`  | `ForeignKey → Save`    | The voted-on save.                                |
| `user`       | `ForeignKey → AppUser` | The voting user.                                  |
| `vote_type`  | `CharField`            | `"upvote"` or `"downvote"` (from `VOTE_CHOICES`). |
| `created_at` | `DateTimeField`        | When the vote was cast.                           |

**Meta**: `unique_together = ('save_file', 'user')` - one vote per user per save.

---

## `common` app

### **Event**

A community gaming event created by staff or moderators.

![eventsExample](/docs/_assets/events_example.png)

| Field                       | Type                   | Description                               |
|-----------------------------|------------------------|-------------------------------------------|
| `title`                     | `CharField`            | Event title.                              |
| `event_date`                | `DateTimeField`        | Scheduled date and time.                  |
| `platform`                  | `CharField`            | Relevant platform (or `"All Platforms"`). |
| `description`               | `TextField`            | Event description.                        |
| `status`                    | `CharField`            | `"upcoming"` or `"past"`.                 |
| `created_by`                | `ForeignKey → AppUser` | Staff/moderator who created the event.    |
| `created_at` / `updated_at` | `DateTimeField`        | Timestamps.                               |

**Meta**: ordered by `event_date` (ascending).

---

### **Board**

A top-level forum category (e.g. GENERAL, HELP & SUPPORT).

| Field         | Type            | Description                  |
|---------------|-----------------|------------------------------|
| `name`        | `CharField`     | Board display name.          |
| `slug`        | `SlugField`     | Unique URL slug for routing. |
| `description` | `TextField`     | Optional description.        |
| `created_at`  | `DateTimeField` | Auto-set on creation.        |

---

### **Thread**

A discussion thread within a `Board`, created by any authenticated user.

![threadsExample](/docs/_assets/threads_example.png)

| Field                       | Type                   | Description                                                 |
|-----------------------------|------------------------|-------------------------------------------------------------|
| `board`                     | `ForeignKey → Board`   | The parent board. Cascades on delete.                       |
| `title`                     | `CharField`            | Thread title.                                               |
| `slug`                      | `SlugField`            | Auto-generated from title via `slugify`.                    |
| `author`                    | `ForeignKey → AppUser` | Thread creator.                                             |
| `is_pinned`                 | `BooleanField`         | Pinned threads appear at the top. Default `False`.          |
| `is_locked`                 | `BooleanField`         | Locked threads cannot receive new replies. Default `False`. |
| `created_at` / `updated_at` | `DateTimeField`        | Timestamps.                                                 |

**Meta**: `unique_together = ['board', 'slug']`. Ordered by `-is_pinned`, `-updated_at`.

---

### **Post**

A single message within a `Thread`. The first post is considered the "OP" (original post).

![postExample](/docs/_assets/post_example.png)

| Field                       | Type                   | Description                            |
|-----------------------------|------------------------|----------------------------------------|
| `thread`                    | `ForeignKey → Thread`  | The parent thread. Cascades on delete. |
| `author`                    | `ForeignKey → AppUser` | Post author.                           |
| `content`                   | `TextField`            | Post body text.                        |
| `created_at` / `updated_at` | `DateTimeField`        | Timestamps.                            |

**Meta**: ordered by `created_at` (ascending - chronological order).

---

#### Next Page: [Permissions](003_permissions.md)

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


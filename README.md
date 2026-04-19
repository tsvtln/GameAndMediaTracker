# CheckPoint - Documentation

### A retro-flavored community platform for ROM enthusiasts. Upload, discover, and discuss ROMs, save files, BIOS files, and screenshots. All in one place!

![banner](/docs/_assets/banner.jpg)

---

## Project Overview

**CheckPoint** is a Django-based web application that acts as a hub for retro and PC gaming fans.  
Users can upload and download ROMs, save files, and BIOS files, share in-game screenshots, 
participate in community forums, and follow upcoming gaming events and it's all wrapped in a pixel-art, NES-inspired UI.

The project is structured as a standard Django application with additional integration of Celery + Redis for async task processing,
PostgreSQL as the database, and WhiteNoise for static file serving.

---

## Contents

### For SoftUni the Project Reviewer

- [Live Demo & Test Credentials](docs/000_softuni_project_reviewer.md)

---

### Setup Tutorials

- [Project Setup](docs/001_project_setup.md)

---

### Key Parts

- [Models](docs/002_models.md)
- [Permissions](docs/003_permissions.md)
- [Signals](docs/004_signals.md)
- [Tasks (Async / Celery)](docs/005_tasks.md)

---

## Django Apps Overview

| App        | Responsibility                                                      |
|------------|---------------------------------------------------------------------|
| `accounts` | Custom user model, profiles, screenshots, favorites                 |
| `roms`     | ROM uploads, comments, reviews, review likes, ROM favorites         |
| `bios`     | BIOS file uploads and downloads                                     |
| `saves`    | Save file uploads, voting system, saves vault                       |
| `common`   | Home, about, events, forums (boards / threads / posts), error pages |

---

## Key Components

### 1. Custom User & Profile System
- `AppUser` extends Django's `AbstractUser` with email + username authentication.
- A `Profile` is automatically created via Django signals on registration, including statistics counters 
(`saves_count`, `screenshots_count`, `favorites_count`).
- Users are automatically assigned to the **Regular Users** group on registration.
- Three user groups exist: **Regular Users**, **Moderators**, **Verified Users** each with different platform permissions.

### 2. ROMs App
- Users can upload ROMs with box art, platform, genre, tags, and an optional description.
- Each ROM supports **comments** and **star reviews** (1–5). The aggregate rating is automatically recalculated 
via Django signals and Celery tasks.
- ROMs can be **favorited**. Download counts are tracked asynchronously.

### 3. BIOS App
- BIOS file uploads are **restricted to Moderators and Verified Users** only.
- Files are grouped and displayed by platform.
- Delete permissions are restricted to the uploader, staff, and moderators.

### 4. Saves App
- Users upload save files with metadata: game title, platform, save type, progress, and completion percentage.
- An **upvote / downvote** voting system.
- A personal **Saves Vault** shows the user's own uploaded saves with total storage stats.
- Download counts are tracked asynchronously.

### 5. Screenshots
- Any authenticated user can upload screenshots tagged with a game name and platform.
- Screenshots can be **favorited** (users cannot favorite their own).
- Favorite/like counters are synced asynchronously via Celery.
- Pages: Latest, Top Rated, My Screenshots.

### 6. Community - Events & Forums
- **Events**: Staff and Moderators can create/delete events and mark them as passed.
- **Forums**: Board → Thread → Post hierarchy. Any authenticated user can create threads and reply.
Moderators/Staff can delete threads and posts.
- The **Website News** page fetches and renders the `CHANGELOG.md` live from GitHub.

### 7. Permission Mixins
- Reusable `UserPassesTestMixin` subclasses 
(`OwnerOrModeratorMixin`, `ModeratorOnlyMixin`, `ModeratorOrVerifiedMixin`, `CanDeleteContextMixin`) 
are used across all apps to enforce consistent access control without duplicating logic.

### 8. Async Task Processing (Celery + Redis)
- Rating recalculation, download counter increments, and profile counter syncing are all offloaded to Celery workers.
- A periodic beat task runs every hour to audit and repair profile statistics counters.

---

## External resources

- Emojis from [emojiguide.org](https://emojiguide.org) and [emojidb.org](https://emojidb.org/)
- Base styling from [NES.css](https://github.com/nostalgic-css/NES.css)
- Font: [Press Start 2P](https://www.fontspace.com/press-start-2p-font-f11591) via [Google Fonts](https://fonts.googleapis.com/css?family=Press+Start+2P)

---

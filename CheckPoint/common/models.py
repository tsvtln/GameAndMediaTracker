from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as gtl
from django.utils.text import slugify
from CheckPoint.roms.choices import PLATFORM_CHOICES


class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name=gtl('Event Title')
    )

    event_date = models.DateTimeField(
        verbose_name=gtl('Event Date')
    )

    platform = models.CharField(
        max_length=200,
        choices=PLATFORM_CHOICES + [('All Platforms', 'All Platforms')],
        default='All Platforms',
        verbose_name=gtl('Platform')
    )

    description = models.TextField(
        verbose_name=gtl('Description')
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming',
        verbose_name=gtl('Status')
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name=gtl('Created By')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gtl('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=gtl('Updated At')
    )

    class Meta:
        verbose_name = gtl('Event')
        verbose_name_plural = gtl('Events')
        ordering = ['event_date']

    def __str__(self):
        return f"{self.title} - {self.event_date.strftime('%Y-%m-%d')}"


class Board(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=gtl('Board Name')
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=gtl('Slug')
    )

    description = models.TextField(
        blank=True,
        verbose_name=gtl('Description')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gtl('Created At')
    )

    class Meta:
        verbose_name = gtl('Board')
        verbose_name_plural = gtl('Boards')
        ordering = ['name']

    def __str__(self):
        return self.name


class Thread(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='threads',
        verbose_name=gtl('Board')
    )

    title = models.CharField(
        max_length=255,
        verbose_name=gtl('Title')
    )

    slug = models.SlugField(
        max_length=255,
        verbose_name=gtl('Slug')
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='threads',
        verbose_name=gtl('Author')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gtl('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=gtl('Updated At')
    )

    is_pinned = models.BooleanField(
        default=False,
        verbose_name=gtl('Pinned')
    )

    is_locked = models.BooleanField(
        default=False,
        verbose_name=gtl('Locked')
    )

    class Meta:
        verbose_name = gtl('Thread')
        verbose_name_plural = gtl('Threads')
        ordering = ['-is_pinned', '-updated_at']
        unique_together = ['board', 'slug']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Post(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=gtl('Thread')
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=gtl('Author')
    )

    content = models.TextField(
        verbose_name=gtl('Content')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gtl('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=gtl('Updated At')
    )

    class Meta:
        verbose_name = gtl('Post')
        verbose_name_plural = gtl('Posts')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

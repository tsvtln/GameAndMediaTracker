from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from CheckPoint.roms.choices import PLATFORM_CHOICES, GENRE_CHOICES


class Rom(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_('Game Title')
    )
    
    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        verbose_name=_('Platform')
    )

    genre = models.CharField(
        max_length=50,
        choices=GENRE_CHOICES,
        verbose_name=_('Genre')
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Description')
    )
    
    rom_file = models.FileField(
        upload_to='roms/%Y/%m/',
        validators=[FileExtensionValidator(
            allowed_extensions=['zip', '7z', 'rar', 'nes', 'sfc', 'gba', 'iso', 'smd', 'bin', 'cue']
        )],
        verbose_name=_('ROM File'),
        help_text=_('Max size: 500MB. Allowed formats: .zip .7z .rar .nes .sfc .gba .iso')
    )
    
    box_art = models.ImageField(
        upload_to='box_art/%Y/%m/',
        verbose_name=_('Box Art'),
        help_text=_('Game box art image (required)')
    )
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_roms',
        verbose_name=_('Uploaded By')
    )
    
    downloads = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Downloads')
    )
    
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        verbose_name=_('Rating')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Uploaded At')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    
    class Meta:
        verbose_name = _('ROM')
        verbose_name_plural = _('ROMs')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} ({self.platform})"
    
    def increment_downloads(self):
        self.downloads += 1
        self.save(update_fields=['downloads'])

    def update_rating(self):
        """Update ROM rating based on average of all reviews"""
        from django.db.models import Avg
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            self.rating = round(avg_rating, 1)
        else:
            self.rating = 0.0
        self.save(update_fields=['rating'])


class Comment(models.Model):
    rom = models.ForeignKey(
        Rom,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('ROM')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rom_comments',
        verbose_name=_('User')
    )

    text = models.TextField(
        verbose_name=_('Comment Text')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created_at']

    def __str__(self):
            return f"{self.user.username}: {self.text[:50]}"


class Review(models.Model):
    rom = models.ForeignKey(
        Rom,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('ROM')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rom_reviews',
        verbose_name=_('User')
    )

    rating = models.PositiveIntegerField(
        verbose_name=_('Rating'),
        help_text=_('Rating from 1 to 5')
    )

    text = models.TextField(
        verbose_name=_('Review Text')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']
        unique_together = ['rom', 'user']  # one review per user per ROM

    def __str__(self):
        return f"{self.user.username}: {self.rating}⭐ - {self.text}"

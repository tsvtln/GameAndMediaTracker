from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import AppUserManager


class AppUser(AbstractUser):
    # custom user model extending Django's AbstractUser.
    # we use email as the primary authentication field.
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('Email Address'),
        help_text=_('Required. Must be a valid email address.')
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_('Username'),
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates if the user can login to admin features.')
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = AppUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.email})"


class Profile(models.Model):

    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )

    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_('Avatar'),
        help_text=_('Upload a profile picture.')
    )

    # ==========
    # Statistics
    # ==========
    favorites_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Favorites Count'),
        help_text=_('Total number of favorited items.')
    )

    saves_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Saves Count'),
        help_text=_('Total number of uploaded saves.')
    )

    screenshots_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Screenshots Count'),
        help_text=_('Total number of uploaded screenshots.')
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
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def increment_favorites(self):
        self.favorites_count += 1
        self.save(update_fields=['favorites_count'])

    def decrement_favorites(self):
        if self.favorites_count > 0:
            self.favorites_count -= 1
            self.save(update_fields=['favorites_count'])

    def increment_saves(self):
        self.saves_count += 1
        self.save(update_fields=['saves_count'])

    def decrement_saves(self):
        if self.saves_count > 0:
            self.saves_count -= 1
            self.save(update_fields=['saves_count'])

    def increment_screenshots(self):
        self.screenshots_count += 1
        self.save(update_fields=['screenshots_count'])

    def decrement_screenshots(self):
        if self.screenshots_count > 0:
            self.screenshots_count -= 1
            self.save(update_fields=['screenshots_count'])


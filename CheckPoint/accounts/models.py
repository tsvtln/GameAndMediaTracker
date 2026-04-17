from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as gtl
from CheckPoint.accounts.managers import AppUserManager
from CheckPoint.accounts.choices import PLATFORM_CHOICES


class AppUser(AbstractUser):
    # custom user model extending Django's AbstractUser.
    # we use email as the primary authentication field.
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=gtl('Email Address'),
        help_text=gtl('Required. Must be a valid email address.')
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=gtl('Username'),
        help_text=gtl('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    )

    is_staff = models.BooleanField(
        gtl('staff status'),
        default=False,
        help_text=gtl('Designates if the user can login to admin features.')
    )

    is_active = models.BooleanField(
        gtl('active'),
        default=True,
        help_text=gtl(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = AppUserManager()

    class Meta:
        verbose_name = gtl('User')
        verbose_name_plural = gtl('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.email})"


class Profile(models.Model):
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=gtl('User')
    )

    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=gtl('Avatar'),
        help_text=gtl('Upload a profile picture.')
    )

    # ==========
    # Statistics
    # ==========
    favorites_count = models.PositiveIntegerField(
        default=0,
        verbose_name=gtl('Favorites Count'),
        help_text=gtl('Total number of favorite items.')
    )

    saves_count = models.PositiveIntegerField(
        default=0,
        verbose_name=gtl('Saves Count'),
        help_text=gtl('Total number of uploaded saves.')
    )

    screenshots_count = models.PositiveIntegerField(
        default=0,
        verbose_name=gtl('Screenshots Count'),
        help_text=gtl('Total number of uploaded screenshots.')
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
        verbose_name = gtl('Profile')
        verbose_name_plural = gtl('Profiles')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def increment_favorites(self):
        Profile.objects.filter(pk=self.pk).update(favorites_count=F('favorites_count') + 1)
        self.refresh_from_db()

    def decrement_favorites(self):
        Profile.objects.filter(pk=self.pk, favorites_count__gt=0).update(favorites_count=F('favorites_count') - 1)
        self.refresh_from_db()

    def increment_saves(self):
        Profile.objects.filter(pk=self.pk).update(saves_count=F('saves_count') + 1)
        self.refresh_from_db()

    def decrement_saves(self):
        Profile.objects.filter(pk=self.pk, saves_count__gt=0).update(saves_count=F('saves_count') - 1)
        self.refresh_from_db()

    def increment_screenshots(self):
        Profile.objects.filter(pk=self.pk).update(screenshots_count=F('screenshots_count') + 1)
        self.refresh_from_db()

    def decrement_screenshots(self):
        Profile.objects.filter(pk=self.pk, screenshots_count__gt=0).update(screenshots_count=F('screenshots_count') - 1)
        self.refresh_from_db()


class Screenshot(models.Model):
    game_name = models.CharField(
        max_length=255,
        verbose_name=gtl('Game Name')
    )

    platform = models.CharField(
        max_length=200,
        choices=PLATFORM_CHOICES,
        verbose_name=gtl('Platform')
    )

    screenshot = models.ImageField(
        upload_to='screenshots/%Y/%m/',
        validators=[FileExtensionValidator(
            allowed_extensions=['png', 'jpg', 'jpeg', 'webp']
        )],
        verbose_name=gtl('Screenshot Image'),
        help_text=gtl('Max size: 5MB. Allowed formats: .png .jpg .jpeg .webp')
    )

    uploaded_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='screenshots',
        verbose_name=gtl('Uploaded By')
    )

    likes = models.PositiveIntegerField(
        default=0,
        verbose_name=gtl('Likes')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gtl('Uploaded At')
    )

    class Meta:
        verbose_name = gtl('Screenshot')
        verbose_name_plural = gtl('Screenshots')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.game_name} - {self.platform} by {self.uploaded_by.username}"


class FavoriteScreenshot(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='favorite_screenshots',
        verbose_name=gtl('User')
    )

    screenshot = models.ForeignKey(
        Screenshot,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name=gtl('Screenshot')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gtl('Favorited At')
    )

    class Meta:
        verbose_name = gtl('Favorite Screenshot')
        verbose_name_plural = gtl('Favorite Screenshots')
        unique_together = ('user', 'screenshot')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.screenshot.game_name}"

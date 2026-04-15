from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as gtl
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from CheckPoint.saves.choices import SAVE_PLATFORM_CHOICES, SAVE_TYPE_CHOICES, PROGRESS_CHOICES, VOTE_CHOICES


class Save(models.Model):
    game_title = models.CharField(
        max_length=255,
        verbose_name=gtl('Game Title')
    )

    platform = models.CharField(
        max_length=200,
        choices=SAVE_PLATFORM_CHOICES,
        verbose_name=gtl('Platform')
    )

    save_type = models.CharField(
        max_length=200,
        choices=SAVE_TYPE_CHOICES,
        verbose_name=gtl('Save Type')
    )

    progress = models.CharField(
        max_length=200,
        choices=PROGRESS_CHOICES,
        verbose_name=gtl('Game Progress')
    )

    mission_detail = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=gtl('Mission Detail'),
        help_text=gtl('Specific mission or checkpoint (optional)')
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=gtl('Description')
    )

    completion = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=gtl('Completion Percentage')
    )

    save_file = models.FileField(
        upload_to='saves/%Y/%m/',
        validators=[FileExtensionValidator(
            allowed_extensions=['zip', 'rar', '7z', 'sav', 'srm', 'state', 'dat']
        )],
        verbose_name=gtl('Save File'),
        help_text=gtl('Max size: 50MB. Allowed formats: .zip .rar .7z .sav .srm .state .dat')
    )

    save_image = models.ImageField(
        upload_to='saves/images/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=gtl('Save Image'),
        help_text=gtl('Optional screenshot or cover image')
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_saves',
        verbose_name=gtl('Uploaded By')
    )

    downloads = models.PositiveIntegerField(
        default=0,
        verbose_name=gtl('Downloads')
    )

    upvotes = models.PositiveIntegerField(
        default=0,
        verbose_name=gtl('Upvotes')
    )

    downvotes = models.PositiveIntegerField(
        default=0,
        verbose_name=gtl('Downvotes')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gtl('Uploaded At')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=gtl('Updated At')
    )

    class Meta:
        verbose_name = gtl('Save')
        verbose_name_plural = gtl('Saves')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.game_title} - {self.platform}"

    def increment_downloads(self):
        self.downloads += 1
        self.save(update_fields=['downloads'])

    @property
    def rating(self):
        total_votes = self.upvotes + self.downvotes
        if total_votes == 0:
            return 0
        return round((self.upvotes / total_votes) * 5, 1)


class SaveVote(models.Model):
    save_file = models.ForeignKey(
        Save,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=gtl('Save')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='save_votes',
        verbose_name=gtl('User')
    )

    vote_type = models.CharField(
        max_length=10,
        choices=VOTE_CHOICES,
        verbose_name=gtl('Vote Type')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gtl('Voted At')
    )

    class Meta:
        verbose_name = gtl('Save Vote')
        verbose_name_plural = gtl('Save Votes')
        unique_together = ('save_file', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.vote_type} on {self.save_file.game_title}"


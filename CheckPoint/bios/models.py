from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as gtl
from django.core.validators import FileExtensionValidator
from CheckPoint.bios.choices import SOURCE_CHOICES
from CheckPoint.roms.choices import PLATFORM_CHOICES


class Bios(models.Model):
    BIOS_PLATFORM_CHOICES = PLATFORM_CHOICES.copy()
    extra_bios_platforms = [
        ('MAME', 'MAME'),
        ('FinalBurn NEO', 'FinalBurn NEO'),
        ('RetroArch', 'RetroArch'),
    ]
    BIOS_PLATFORM_CHOICES.extend(xtra for xtra in extra_bios_platforms)

    platform = models.CharField(
        max_length=255,
        choices=BIOS_PLATFORM_CHOICES,
        verbose_name=gtl('Platform')
    )
    
    bios_file = models.FileField(
        upload_to='bios/%Y/%m/',
        validators=[FileExtensionValidator(
            allowed_extensions=['bin', 'rom', 'zip', 'gz', 'pup']
        )],
        verbose_name=gtl('BIOS File'),
        help_text=gtl('Max size: 5GB. Allowed formats: .bin .rom .zip .tar.gz .pup')
    )
    
    description = models.TextField(
        verbose_name=gtl('Description'),
        help_text=gtl('Description of the BIOS file(s)')
    )
    
    source = models.CharField(
        max_length=255,
        choices=SOURCE_CHOICES,
        verbose_name=gtl('Upload Source')
    )
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_bios',
        verbose_name=gtl('Uploaded By')
    )
    
    downloads = models.PositiveIntegerField(
        default=0,
        verbose_name=gtl('Downloads')
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
        verbose_name = gtl('BIOS')
        verbose_name_plural = gtl('BIOS Files')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.platform} - {self.bios_file.name}"
    
    def increment_downloads(self):
        self.downloads += 1
        self.save(update_fields=['downloads'])

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from CheckPoint.roms.models import Rom, Comment, Review
from CheckPoint.roms.choices import PLATFORM_CHOICES, GENRE_CHOICES


class RomUploadForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        required=True,
        label=_('Game Title'),
        widget=forms.TextInput(attrs={
            'class': 'styled-input',
            'placeholder': 'Super Mario Bros',
        })
    )

    platform = forms.ChoiceField(
        choices=PLATFORM_CHOICES,
        required=True,
        label=_('Platform'),
        widget=forms.Select(attrs={
            'class': 'styled-input',
        })
    )

    genre = forms.ChoiceField(
        choices=GENRE_CHOICES,
        required=True,
        label=_('Genre'),
        widget=forms.Select(attrs={
            'class': 'styled-input',
        })
    )

    description = forms.CharField(
        required=False,
        label=_('Description'),
        widget=forms.Textarea(attrs={
            'class': 'styled-input',
            'rows': 5,
            'placeholder': 'Classic NES platformer where Mario must rescue Princess Peach.',
        })
    )

    rom_file = forms.FileField(
        required=True,
        label=_('ROM File'),
        widget=forms.FileInput(attrs={
            'class': 'upload-file-input',
            'accept': '.zip,.7z,.rar,.nes,.sfc,.gba,.iso',
        })
    )

    box_art = forms.ImageField(
        required=True,
        label=_('Box Art'),
        widget=forms.FileInput(attrs={
            'class': 'upload-file-input',
            'accept': 'image/*',
        })
    )

    class Meta:
        model = Rom
        fields = ('title', 'platform', 'genre', 'description', 'rom_file', 'box_art')

    def clean_rom_file(self):
        rom_file = self.cleaned_data.get('rom_file')
        if rom_file:
            # 500MB = 500 * 1024 * 1024 bytes
            if rom_file.size > 500 * 1024 * 1024:
                raise ValidationError(_('ROM file size cannot exceed 500MB.'))
        return rom_file

    def clean_box_art(self):
        box_art = self.cleaned_data.get('box_art')
        if box_art:
            # max 5MB for box art
            if box_art.size > 5 * 1024 * 1024:
                raise ValidationError(_('Box art image cannot exceed 5MB.'))

            # check file extension
            allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
            ext = box_art.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise ValidationError(
                    _('Unsupported image type. Allowed: JPG, PNG, WEBP.')
                )
        return box_art


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        required=True,
        label=_('Comment'),
        widget=forms.Textarea(attrs={
            'class': 'styled-input',
            'rows': 3,
            'placeholder': 'Write your comment...',
            'id': 'comment-text',
        })
    )

    class Meta:
        model = Comment
        fields = ('text',)


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        required=True,
        label=_('Rating'),
        min_value=1,
        max_value=5,
        widget=forms.HiddenInput(attrs={
            'id': 'review-rating-value',
        })
    )

    text = forms.CharField(
        required=True,
        label=_('Review'),
        widget=forms.Textarea(attrs={
            'class': 'styled-input',
            'rows': 3,
            'placeholder': 'Write your review...',
            'id': 'review-text',
        })
    )

    class Meta:
        model = Review
        fields = ('rating', 'text')

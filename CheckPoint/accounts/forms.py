from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gtl
from CheckPoint.accounts.models import AppUser, Profile, Screenshot
from CheckPoint.accounts.choices import PLATFORM_CHOICES
from CheckPoint.accounts.validators import validate_password_strength
import re


class AppUserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label=gtl('Username'),
        help_text=gtl('150 characters or fewer. Letters, digits and @.+-_ only.'),
        widget=forms.TextInput(attrs={
            'class': 'styled-input',
            'placeholder': 'username',
            'autocomplete': 'username',
        })
    )

    email = forms.EmailField(
        max_length=255,
        required=True,
        label=gtl('Email Address'),
        widget=forms.EmailInput(attrs={
            'class': 'styled-input',
            'placeholder': 'your.email@example.com',
            'autocomplete': 'email',
        })
    )

    password1 = forms.CharField(
        label=gtl('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'styled-input',
            'placeholder': 'Enter password',
            'autocomplete': 'new-password',
        }),
        help_text=gtl(
            'At least 8 characters with 1 uppercase, 1 lowercase, 1 number and 1 special symbol (@#$%^&+=!)'
        )
    )

    password2 = forms.CharField(
        label=gtl('Password Confirmation'),
        widget=forms.PasswordInput(attrs={
            'class': 'styled-input',
            'placeholder': 'Re-enter password',
            'autocomplete': 'new-password',
        }),
        help_text=gtl('Repeat the password.')
    )

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        return validate_password_strength(password)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if AppUser.objects.filter(username=username).exists():
            raise ValidationError(gtl('This username is already taken.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if AppUser.objects.filter(email=email).exists():
            raise ValidationError(gtl('A user with this email already exists.'))
        return email.lower()


class AppUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=gtl('Username'),
        widget=forms.TextInput(attrs={
            'class': 'styled-input',
            'placeholder': 'username',
            'autocomplete': 'username',
            'autofocus': True,
        })
    )

    password = forms.CharField(
        label=gtl('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'styled-input',
            'placeholder': 'Enter password',
            'autocomplete': 'current-password',
        })
    )

    error_messages = {
        'invalid_login': gtl('Please enter a correct username and password. Note that both fields are case-sensitive.'),
        'inactive': gtl('This account is inactive.'),
    }


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        label=gtl('Profile Avatar'),
        help_text=gtl('Upload a new profile picture (optional).'),
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        })
    )

    class Meta:
        model = Profile
        fields = ('avatar',)

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # check file size (5*1024*1024 = 5MB)
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError(gtl('Image file size cannot exceed 5MB.'))

            # check file extension to allow only picture formats
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = avatar.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise ValidationError(
                    gtl('Unsupported file type. Allowed types: JPG, PNG, GIF, WEBP.')
                )
        return avatar


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label=gtl('Username'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username',
        })
    )

    email = forms.EmailField(
        max_length=255,
        required=True,
        label=gtl('Email Address'),
        disabled=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
        })
    )

    class Meta:
        model = AppUser
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if AppUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise ValidationError(gtl('This username is already taken.'))
        return username


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=gtl('Current Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'password-modal-input',
            'placeholder': 'Current Password',
            'autocomplete': 'current-password',
        })
    )

    new_password1 = forms.CharField(
        label=gtl('New Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'password-modal-input',
            'placeholder': 'New Password',
            'autocomplete': 'new-password',
        }),
        help_text=gtl(
            'At least 8 characters with 1 uppercase, 1 lowercase, 1 number and 1 special symbol (@#$%^&+=!)'
        )
    )

    new_password2 = forms.CharField(
        label=gtl('Confirm New Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'password-modal-input',
            'placeholder': 'Confirm New Password',
            'autocomplete': 'new-password',
        })
    )

    def clean_new_password1(self):
        """Validate password strength."""
        password = self.cleaned_data.get('new_password1')
        return validate_password_strength(password)


class ScreenshotUploadForm(forms.ModelForm):
    game_name = forms.CharField(
        max_length=255,
        required=True,
        label=gtl('Game Name'),
        widget=forms.TextInput(attrs={
            'class': 'styled-input',
            'placeholder': 'e.g. Chrono Trigger',
        })
    )

    platform = forms.ChoiceField(
        required=True,
        choices=PLATFORM_CHOICES,
        label=gtl('Platform'),
        widget=forms.Select(attrs={
            'class': 'styled-select',
        })
    )

    screenshot = forms.ImageField(
        required=True,
        label=gtl('Screenshot File'),
        widget=forms.FileInput(attrs={
            'class': 'upload-file-input',
            'id': 'screenshot-file',
            'accept': '.png,.jpg,.jpeg,.webp',
        })
    )

    class Meta:
        model = Screenshot
        fields = ('game_name', 'platform', 'screenshot')

    def clean_screenshot(self):
        screenshot = self.cleaned_data.get('screenshot')
        if screenshot:
            # check file size (5MB)
            if screenshot.size > 5 * 1024 * 1024:
                raise ValidationError(gtl('Screenshot file size cannot exceed 5MB.'))

            # check file extension
            allowed_extensions = ['png', 'jpg', 'jpeg', 'webp']
            ext = screenshot.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise ValidationError(gtl('Unsupported file type. Allowed types: PNG, JPG, JPEG, WEBP.'))

        return screenshot

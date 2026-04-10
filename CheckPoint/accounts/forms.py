from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

from .models import AppUser, Profile


class AppUserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_('Username'),
        help_text=_('150 characters or fewer. Letters, digits and @.+-_ only.'),
        widget=forms.TextInput(attrs={
            'class': 'styled-input',
            'placeholder': 'username',
            'autocomplete': 'username',
        })
    )

    email = forms.EmailField(
        max_length=255,
        required=True,
        label=_('Email Address'),
        widget=forms.EmailInput(attrs={
            'class': 'styled-input',
            'placeholder': 'your.email@example.com',
            'autocomplete': 'email',
        })
    )

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'styled-input',
            'placeholder': 'Enter password',
            'autocomplete': 'new-password',
        }),
        help_text=_(
            'At least 8 characters with 1 uppercase, 1 lowercase, 1 number and 1 special symbol (@#$%^&+=!)'
        )
    )

    password2 = forms.CharField(
        label=_('Password Confirmation'),
        widget=forms.PasswordInput(attrs={
            'class': 'styled-input',
            'placeholder': 'Re-enter password',
            'autocomplete': 'new-password',
        }),
        help_text=_('Repeat the password.')
    )

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'))
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(_('Password must contain at least one lowercase letter.'))
        
        if not re.search(r'\d', password):
            raise ValidationError(_('Password must contain at least one number.'))
        
        if not re.search(r'[@#$%^&+=!]', password):
            raise ValidationError(_('Password must contain at least one special symbol (@#$%^&+=!).'))
        
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if AppUser.objects.filter(username=username).exists():
            raise ValidationError(_('This username is already taken.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if AppUser.objects.filter(email=email).exists():
            raise ValidationError(_('A user with this email already exists.'))
        return email.lower()


class AppUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'class': 'styled-input',
            'placeholder': 'username',
            'autocomplete': 'username',
            'autofocus': True,
        })
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'styled-input',
            'placeholder': 'Enter password',
            'autocomplete': 'current-password',
        })
    )

    error_messages = {
        'invalid_login': _(
            'Please enter a correct username and password. Note that both fields are case-sensitive.'
        ),
        'inactive': _('This account is inactive.'),
    }


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        label=_('Profile Avatar'),
        help_text=_('Upload a new profile picture (optional).'),
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
                raise ValidationError(_('Image file size cannot exceed 5MB.'))

            # check file extension to allow only picture formats
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = avatar.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise ValidationError(
                    _('Unsupported file type. Allowed types: JPG, PNG, GIF, WEBP.')
                )
        return avatar


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username',
        })
    )

    email = forms.EmailField(
        max_length=255,
        required=True,
        label=_('Email Address'),
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
            raise ValidationError(_('This username is already taken.'))
        return username


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_('Current Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'password-modal-input',
            'placeholder': 'Current Password',
            'autocomplete': 'current-password',
        })
    )

    new_password1 = forms.CharField(
        label=_('New Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'password-modal-input',
            'placeholder': 'New Password',
            'autocomplete': 'new-password',
        }),
        help_text=_(
            'At least 8 characters with 1 uppercase, 1 lowercase, 1 number and 1 special symbol (@#$%^&+=!)'
        )
    )

    new_password2 = forms.CharField(
        label=_('Confirm New Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'password-modal-input',
            'placeholder': 'Confirm New Password',
            'autocomplete': 'new-password',
        })
    )

    def clean_new_password1(self):
        """Validate password strength."""
        password = self.cleaned_data.get('new_password1')

        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))

        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'))

        if not re.search(r'[a-z]', password):
            raise ValidationError(_('Password must contain at least one lowercase letter.'))

        if not re.search(r'\d', password):
            raise ValidationError(_('Password must contain at least one number.'))

        if not re.search(r'[@#$%^&+=!]', password):
            raise ValidationError(_('Password must contain at least one special symbol (@#$%^&+=!).'))

        return password



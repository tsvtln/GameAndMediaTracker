from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gtl
import re


def validate_password_strength(password):
    if len(password) < 8:
        raise ValidationError(gtl('Password must be at least 8 characters long.'))

    if not re.search(r'[A-Z]', password):
        raise ValidationError(gtl('Password must contain at least one uppercase letter.'))

    if not re.search(r'[a-z]', password):
        raise ValidationError(gtl('Password must contain at least one lowercase letter.'))

    if not re.search(r'\d', password):
        raise ValidationError(gtl('Password must contain at least one number.'))

    if not re.search(r'[@#$%^&+=!]', password):
        raise ValidationError(gtl('Password must contain at least one special symbol (@#$%^&+=!).'))

    return password

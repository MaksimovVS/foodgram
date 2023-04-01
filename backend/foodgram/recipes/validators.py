# recipes/validators.py

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_nonzero(value):
    if value == 0:
        raise ValidationError(
            _('%(value) не может равняться нулю.'),
            params={'value': value},
        )

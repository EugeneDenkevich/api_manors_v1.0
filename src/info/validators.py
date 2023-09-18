from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_geo(value: str):
    if len(value) != 9 or value[2] != '.':
        raise ValidationError(_(
                'Type the valid value. Example: '
                '12.345678. It must contains 8 '
                'digits and a dot after first two'

            ))
    digits = value[0:2] + value[3:9]
    for s in digits:
        if not s.isdigit():
            raise ValidationError(_(
                'Type the valid value. Example: '
                '12.345678. It must contains 8 '
                'digits and a dot after first two'

            ))
        
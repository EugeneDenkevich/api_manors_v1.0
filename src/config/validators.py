import re

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from .settings import (MAX_IMAGE_SIZE, MAX_IMAGE_SIZE_MB)


def validate_image_size(image):
    try:
        if image.size > MAX_IMAGE_SIZE:
            raise ValidationError(
                f'Максмимальный размер изображения должен быть не более {MAX_IMAGE_SIZE_MB} Mb.'
            )
    except FileNotFoundError:
        return
    

def validate_name(image):
    if re.search(r'[а-яА-Я]', image.name):
        raise ValidationError(
            'Russian letters are not allowed'
        )


def get_price_validators():
    return [
        MaxValueValidator(9999.99),
        MinValueValidator(0.0)
    ]

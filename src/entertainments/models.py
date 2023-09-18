from django.db import models

from config.validators import validate_image_size


class Entertainment(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name = 'Название'
    )
    description_short = models.TextField(max_length=300, verbose_name = 'Короткое описание')
    description_long = models.TextField(verbose_name = 'Полное описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Развлечение'
        verbose_name_plural = 'Развлечения'

    def __str__(self):
        return self.title
    

class EntertainmentPrice(models.Model):
    header = models.CharField(max_length=256, verbose_name = 'Услуга')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name = 'Цена',
                                blank=True, null=True)
    entertainment = models.ForeignKey(
        to='Entertainment', on_delete=models.CASCADE, related_name='prices')

    class Meta:
        verbose_name = 'Entertainment price'
        verbose_name_plural = 'Услуги и цены'

    def __str__(self):
        return ''


class PhotoEntertainment(models.Model):
    file = models.ImageField(
        upload_to='photo_entertainment',
        null=True, blank=True,
        verbose_name='Фото',
        validators=[validate_image_size]
    )
    entertainment = models.ForeignKey(
        to='Entertainment',
        on_delete=models.CASCADE,
        related_name='photos'
    )

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return ''
    

class NearestPlace(models.Model):
    title = models.CharField(max_length=256, verbose_name = u'Название')
    description = models.TextField(max_length=1000, verbose_name = u'Описание',
                                   blank=True, null=True)
    location = models.TextField(max_length=1000, verbose_name = u'Местонахождение',
                                blank=True, null=True)

    class Meta:
        verbose_name = u'Место'
        verbose_name_plural = u'Ближайшие места'

    def __str__(self):
        return self.title


class PhotoNearestPlace(models.Model):
    file = models.ImageField(
        upload_to='photo_nearest_places',
        null=True,
        blank=True,
        verbose_name='Файл',
        validators=[validate_image_size]
    )
    places = models.ForeignKey(
        to="NearestPlace",
        on_delete=models.CASCADE,
        related_name='photos'
    )

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return ''


class Galery(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'

    def __str__(self):
        return self.title


class PhotoGalery(models.Model):
    file = models.ImageField(
        upload_to='photo_galery',
        null=True,
        blank=True,
        verbose_name='Файл',
        validators=[validate_image_size]
    )
    galeries = models.ForeignKey(
        to="Galery",
        on_delete=models.CASCADE,
        related_name='photos'
    )

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return ''
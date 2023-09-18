from django.db import models


SOCIAL_CHOICES = [
    ('Facebook', 'Facebook'),
    ('Instagram', 'Instagram'),
]
CURRENCIES = [
    ('byn', 'BYN'),
    ('rub', 'RUB'),
    ('usd', 'USD'),
    ('eur', 'EUR'),
]


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class Info(SingletonModel):
    currency = models.CharField(
        choices=CURRENCIES, max_length=4, verbose_name=u'Валюта', default='byn')
    address = models.TextField(max_length=1000, verbose_name=u'Адрес')
    comment = models.TextField(
        max_length=1000, verbose_name=u'Комментарий', blank=True, null=True)
    latitude = models.CharField(
        max_length=10, verbose_name='Широта', blank=True, null=True)
    longitude = models.CharField(
        max_length=10, verbose_name='Долгота', blank=True, null=True)
    was_changed = models.DateField(auto_now=True, verbose_name=u'Изменено')

    class Meta:
        verbose_name = 'Общая информация'
        verbose_name_plural = 'Общая информация'

    def __str__(self):
        return f'Информация'

    def social(self) -> dict:
        """
        Returns icons and links for each social of info-card
        """
        socials_objects = self.socials.all()
        social = [{s.type: s.link} for s in socials_objects]
        return social


class PhoneNumber(models.Model):
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    info = models.ForeignKey(
        to='Info',
        related_name='phones',
        on_delete=models.CASCADE,
        verbose_name='phone'
    )

    class Meta:
        verbose_name = u'Телефон'
        verbose_name_plural = u'Телефоны'

    def __repr__(self):
        return self.phone

    def __str__(self):
        return ''


class InfoSocial(models.Model):
    type = models.CharField(
        max_length=256,
        choices=SOCIAL_CHOICES,
        verbose_name=u'Соц. сеть'
    )
    link = models.TextField()
    info = models.ForeignKey(
        to='Info',
        related_name='socials',
        on_delete=models.CASCADE,
        verbose_name='info'
    )

    class Meta:
        verbose_name = u'Соц. сеть'
        verbose_name_plural = u'Соц. сети'

    def __str__(self):
        return ''


class FeedingInfo(SingletonModel):
    was_changed = models.DateField(auto_now=True, verbose_name=u'Изменено')

    class Meta:

        verbose_name = u'О питании'
        verbose_name_plural = u'О питании'

    def __str__(self):
        return u'Общая'


class Meal(models.Model):
    title = models.CharField(max_length=256, verbose_name=u'Название')
    time = models.TimeField(verbose_name=u'Время')
    price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=u'Стоимость')
    feeding = models.ForeignKey(
        to='FeedingInfo', on_delete=models.CASCADE, related_name='meals')

    class Meta:

        verbose_name = u'Приём пищи'
        verbose_name_plural = u'Приёмы пищи'

    def __str__(self):
        return u'Приём пищи'


class Dish(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name=u'Название'
    )
    description = models.TextField(
        verbose_name=u'Описание', null=True, blank=True,)
    photo = models.ImageField(
        upload_to='photo_dish',
        null=True,
        blank=True,
        verbose_name='Фото'
    )
    feeding = models.ForeignKey(
        to='FeedingInfo', on_delete=models.CASCADE, related_name='dishes')

    class Meta:
        verbose_name = u'Блюдо'
        verbose_name_plural = u'Кухня'

    def __str__(self):
        return self.title


class RulesInfo(SingletonModel):
    was_changed = models.DateField(auto_now=True, verbose_name=u'Изменено')

    class Meta:
        verbose_name = 'Правила'
        verbose_name_plural = 'Правила'

    def __str__(self):
        return f'Правила'


class Rule(models.Model):
    content = models.TextField(max_length=80, verbose_name='Содержание')
    rules = models.ForeignKey(to='RulesInfo', related_name='rule',
                              on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(
        auto_now=True, auto_created=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Правило'
        verbose_name_plural = 'Правила'

    def __str__(self):
        return f'изменено {self.created_at}'

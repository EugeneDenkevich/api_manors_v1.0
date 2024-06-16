from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from config.validators import validate_image_size
from config.settings import MAX_NUMBER_OF_GUESTS
from config.utils.custom import feature_divided

from config.validators import get_price_validators

FEATURES_CHOICES = [
    ('Wifi', 'Бесплатный Wi-Fi'),
    ('Free parking', 'Бесплатная парковка'),
    ('Terrace', 'Терасса'),
    ('Balcony', 'Балкон'),
    ('Conditioner', 'Кондиционер'),
    ('TV', 'Телевизор'),
    ('Patio', 'Патио'),
    ('Brazier', 'Мангал'),
    ('Personal pier', 'Личный пирс'),
    
    ('Kitchen', 'Кухня'),
    ('Fridge', 'Холодильник'),
    ('Dishes', 'Посуда'),
    ('Stove', 'Плита'),
    ('Microwave', 'Микроволновая печь'),
    ('Dishwasher', 'Посудомоечная машина'),

    ('Furniture for babies', 'Мебель для грудных детей'),
    ('Shower/Bath', 'Душ/Ванна'),
    ('Washing machine', 'Стиральная машина'),
    ('Iron', 'Утюг'),
    ('Hair dryer', 'Фен'),
]

SEX_CHOICES = [
    ('Мужской', 'Мужской'),
    ('Женский', 'Женский'),
]

BEDS = [
    ('sgb', 'Односпальная'),
    ('dbb', 'Двухспальная'),
    ('exb', 'Дополнительная'),
    ('crb', 'Детская'),
]

ROOMS = [
    ('bedroom', 'Спальня'),
]

PURCHASE_STATUSES = [
    ('New', 'Новая'),
    ('Approved', 'Одобрена'),
    ('Denied', 'Отклонена'),
    ('Closed', 'Завершена'),
]


class Object(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    pers_num = models.IntegerField(
        verbose_name='Вместимость',
        validators=[MaxValueValidator(
            MAX_NUMBER_OF_GUESTS), MinValueValidator(1)],
    )
    description_short = models.TextField(
        max_length=256,
        verbose_name='Короткое описание'
    )
    description_long = models.TextField(
        verbose_name='Подробное описание',
        blank=True,
        null=True
    )
    price_weekday = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        verbose_name='Цена от',
        validators=get_price_validators(),
    )
    price_holiday = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        verbose_name='Цена до',
        validators=get_price_validators(),
    )
    created_date = models.DateField(
        auto_now_add=True, verbose_name='Дата добавления')
    is_reserved = models.BooleanField(default=False, verbose_name='Занят')

    class Meta:
        verbose_name = 'Домик'
        verbose_name_plural = 'Домики'

    class Meta:
        verbose_name = 'Домик'
        verbose_name_plural = 'Домики'

    def __str__(self):
        return self.title

    @property
    def has_approved_purchases(self):
        purchases = self.purchases.filter(stat='Approved')
        return False if len(purchases) == 0 else True


class PhotoObject(models.Model):
    file = models.ImageField(
        upload_to='photo_object',
        null=True,
        blank=True,
        verbose_name='Файл',
        validators=[validate_image_size]
    )
    object_id = models.ForeignKey(
        to="Object",
        on_delete=models.CASCADE,
        related_name='photos'
    )

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return f'{self.file.url}'


class Room(models.Model):
    type = models.CharField(
        max_length=20, choices=ROOMS, verbose_name='Комната')
    object_id = models.ForeignKey(
        to="Object",
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    class Meta:

        verbose_name = 'Objects room'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return self.type.capitalize()


class ObjectFeature(models.Model):
    type = models.CharField(
        max_length=256,
        choices=feature_divided(),
        verbose_name='Тип услуги'
    )

    object_id = models.ForeignKey(
        to='Object',
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name='Object'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.type

    def save(self, *args, **kwargs):
        features = self.object_id.features.all()
        features_types = [f.type for f in features]
        if self.type in features_types:
            return
        return super().save(*args, **kwargs)


class Purchase(models.Model):
    object = models.ForeignKey(
        to="Object", related_name="purchases", on_delete=models.CASCADE, verbose_name='Домик',
        null=True)
    fio = models.CharField(
        max_length=300,
        verbose_name=u'ФИО',
        validators=[RegexValidator(regex=r'^([a-zA-Zа-яА-Я]+\s*){1,3}$',
                    message='Используйе только буквы латиницу или крилицу.')],
        help_text='Примеры: Грибников Семён Олегович, Грибников Семён'
    )
    passport_country = models.CharField(
        max_length=256, verbose_name=u'Гражданство',
        validators=[RegexValidator(regex=r'^[a-zA-Zа-яА-Я\s]+$',
                    message='Используйте только кирилицу или латиницу.')],
        help_text='Примеры: Беларусь, Россия, Украина')
    address = models.TextField(verbose_name=u'Адрес')
    phone_number = models.CharField(max_length=256, verbose_name=u'Телефон',
                                    validators=[RegexValidator(regex=r'^[+]?\d{1,5}\s?[\(-]?\d{1,5}[\)-]?\s?(\d{1,5}-?){1,5}\d{1,5}$',
                                                               message='Введите корректный номер телефона')],
                                    help_text='Примеры: +375(29)123-12-12, 375291231212, 8(029)1231212, 80291231212')
    email = models.EmailField(verbose_name=u'Email',
                              help_text='Пример: user@example.com')
    telegram = models.CharField(
        max_length=256, verbose_name=u'Ник Телеграм', blank=True, null=True)
    desired_arrival = models.DateField(verbose_name=u'Дата заселения')
    desired_departure = models.DateField(verbose_name=u'Дата выселения')
    status = models.BooleanField(default=False, verbose_name=u'Статус')
    stat = models.CharField(
        max_length=20, choices=PURCHASE_STATUSES, default='New',
        verbose_name=u'Статус'
    )
    is_finished = models.BooleanField(default=False, verbose_name=u'Завершена')
    was_object = models.ForeignKey(
        to="Object", related_name="was_purchases", on_delete=models.CASCADE,
        verbose_name='Ранее в заказе', blank=True, null=True)
    count_adult = models.IntegerField('Кол-во взрослых',
                                      validators=[MinValueValidator(1),
                                                  MaxValueValidator(20)],
                                      help_text='От 1 до 20')
    count_kids = models.IntegerField('Кол-во детей до 10 лет',
                                     validators=[MinValueValidator(0),
                                                 MaxValueValidator(20)],
                                     help_text='От 0 до 20')
    pets = models.TextField('Инфо о животных', blank=True, null=True)
    comment = models.TextField('Комментарий закзачика', blank=True, null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'Заявка #{self.pk}'

    def save(self, *args, **kwargs):
        self.passport_country = self.passport_country.capitalize()
        super(Purchase, self).save(*args, **kwargs)


class Bed(models.Model):
    type = models.CharField(choices=BEDS, max_length=40,
                            verbose_name='Кровать')
    object_id = models.ForeignKey(
        to='Object', related_name='beds', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Кровать'
        verbose_name_plural = 'Кровати'

    def __str__(self):
        return self.type

from django.db import models

from config.validators import validate_image_size, validate_name


class Singleton(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(Singleton, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class MainPage(Singleton):
    title = models.CharField(max_length=256, default='Заповедный остров',
                             verbose_name='Название сайта')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    house_title = models.CharField(max_length=256, default='Домики',
                                   verbose_name='Домики')
    house_description = models.TextField(blank=True, null=True,
                                         verbose_name='Описание')
    kitchen_title = models.CharField(max_length=256, default='Кухня',
                                     verbose_name='Кухня')
    kitchen_description = models.TextField(blank=True, null=True,
                                           verbose_name='Описание')
    entertainment_title = models.CharField(max_length=256, default='Развлечения',
                                           verbose_name='Развлечения')
    entertainment_description = models.TextField(blank=True, null=True,
                                                 verbose_name='Описание')
    was_changed = models.DateField(auto_now=True, verbose_name=u'Изменено')

    def __str__(self):
        return 'Главная страница'
    
    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница' 
    

class PhotoMainPage(models.Model):
    file = models.ImageField(
        upload_to='photo_main_page',
        null=True,
        blank=True,
        verbose_name='Файл',
        validators = [validate_image_size]
    )
    main_page = models.ForeignKey(
        to='MainPage',
        related_name='photos',
        verbose_name='Main Page Photo',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
    
    def __str__(self):
        return ''
    

class BackPhoto(Singleton):
    photo_m = models.ImageField(upload_to='photo_pages',
                                validators=[validate_image_size,
                                            validate_name], verbose_name='Фон Главная',
                                blank=True, null=True)
    photo_h = models.ImageField(upload_to='photo_pages',
                                validators=[validate_image_size,
                                            validate_name], verbose_name='Фон Домики',
                                blank=True, null=True)
    photo_k = models.ImageField(upload_to='photo_pages',
                                validators=[validate_image_size,
                                            validate_name], verbose_name='Фон Кухня',
                                blank=True, null=True)
    photo_e = models.ImageField(upload_to='photo_pages',
                                validators=[validate_image_size,
                                            validate_name], verbose_name='Фон Развлечения',
                                blank=True, null=True)
    was_changed = models.DateField(auto_now=True, verbose_name=u'Изменено')

    class Meta:
        verbose_name = 'Фоновые фото'
        verbose_name_plural = 'Фоновые фото'

    def __str__(self):
        return ''


class PolicyAgreement(Singleton):
    policy = models.TextField(verbose_name='Политика конфиденциальности',
                              blank=True, null=True)
    agreement = models.TextField(verbose_name='Пользовательское соглашение',
                                 blank=True, null=True)
    was_changed = models.DateField(auto_now=True, verbose_name=u'Изменено')

    class Meta:
        verbose_name = 'Политика и соглашение'
        verbose_name_plural = 'Политика и соглашение'

    def __str__(self):
        return ''

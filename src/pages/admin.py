from typing import Any
import re

from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django import forms
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from django.core.exceptions import ValidationError

from config.utils import manual_formsets
from . import models


class MainPageForm(forms.ModelForm):
    house_title = forms.CharField(max_length=256, label = u'Домики',
                                  help_text='Можете указать своё название для раздела "Домики"')
    kitchen_title = forms.CharField(max_length=256, label = u'Кухня',
                                    help_text='Можете указать своё название для раздела "Кухня"')
    entertainment_title = forms.CharField(max_length=256, label = u'Развлечения',
                                          help_text='Можете указать своё название для раздела "Развлечения"')
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), 
                                  label = u'Описание', required=False,
                                  help_text='Расскажите о своей усадьбе')
    house_description = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), 
                                        label = u'Описание', required=False,
                                        help_text='В этом блоке изложите общую информацию о ваших домиках.')
    kitchen_description = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), 
                                          label = u'Описание', required=False,
                                          help_text='Расскажите об особеностях вашей кухни в этом блоке.')
    entertainment_description = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), 
                                                label = u'Описание', required=False,
                                                help_text='Расскажите здесь, чем вы будете '
                                                          'равзлекать своих гостей.')


class PhotoObjectFrom(forms.ModelForm):
    file = forms.ImageField(widget=AdminFileWidget)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if re.search(r'[а-яА-Я]', file.name):
            raise ValidationError(
                'Russian letters are not allowed'
            )
        return file


class PhotoMainPageTabularInline(admin.TabularInline):
    model = models.PhotoMainPage
    extra = 0
    fields = ['preview', 'file']
    readonly_fields = ['preview']
    form = PhotoObjectFrom

    def preview(self, obj):
        if obj.file:
            img = get_thumbnail(obj.file, '70x70',
                                crop='center', quality=99)
            return mark_safe(f'<img src="{img.url}">')

    preview.short_description = u"Фото"
    preview.allow_tags = True


@admin.register(models.MainPage)
class MainPageAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Заглавие сайта',
            {
                'fields':
                [
                    'title',
                    'description',

                ]
            },
        ),
        (
            'Домики',
            {
                'fields':
                [
                    'house_title',
                    'house_description',
                ]
            },
        ),
        (
            'Кухня',
            {
                'fields': [
                    'kitchen_title',
                    'kitchen_description',
                ]
            },
        ),
        ( 
            'Развлечения',
            {
                'fields': [
                    'entertainment_title',
                    'entertainment_description',
                ]
            },
        )
    ]
    list_display = [
        'change',
        'was_changed',
    ]
    inlines = [
        PhotoMainPageTabularInline
    ]
    form = MainPageForm

    @admin.display(description='')
    def change(self, obj):
        return mark_safe('<b>Изменить</b>')

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            models.MainPage.load().save()
        except Exception:
            pass

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_inline_formsets(self, request, formsets,
                            inline_instances, obj: Any | None = ...):
        inline_admin_formsets = super().get_inline_formsets(
            request, formsets, inline_instances, obj)
        return manual_formsets.improve_inline_formset(inline_admin_formsets)


class BackPhotoAdminFileWidget(AdminFileWidget):
    template_name = 'admin/widgets/backphoto_clearable_file_input.html'


class BackPhotoFrom(forms.ModelForm):
    photo_m = forms.ImageField(widget=BackPhotoAdminFileWidget,
                               required=False,
                               label='Фон Главная')
    photo_h = forms.ImageField(widget=BackPhotoAdminFileWidget,
                               required=False,
                               label='Фон Домики')
    photo_k = forms.ImageField(widget=BackPhotoAdminFileWidget,
                               required=False,
                               label='Фон Кухня')
    photo_e = forms.ImageField(widget=BackPhotoAdminFileWidget,
                               required=False,
                               label='Фон Развлечения')


@admin.register(models.BackPhoto)
class BackPhotoModelAdmin(admin.ModelAdmin):
    list_display = [
        'change',
        'was_changed',
    ]
    form = BackPhotoFrom

    def has_add_permission(self, request, obj=None):
        return False
 
    def has_delete_permission(self, request, obj=None):
        return False

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            models.BackPhoto.load().save()
        except Exception:
            pass

    @admin.display(description='')
    def change(self, object):
        return mark_safe(f'<b>Изменить</b>')
    

class PolicyAgreementForm(forms.ModelForm):
    policy = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':6}),
                             label='Политика конфиденциальности', required=True)
    agreement = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':6}),
                                label='Пользовательское соглашение', required=True)


@admin.register(models.PolicyAgreement)
class PolicyAgreementModelAdmin(admin.ModelAdmin):
    list_display = [
        'change',
        'was_changed',
    ]
    form = PolicyAgreementForm

    @admin.display(description='')
    def change(self, object):
        return mark_safe(f'<b>Изменить</b>')

    def has_add_permission(self, request, object=None):
        return False

    def has_delete_permission(self, request, object=None):
        return False

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            models.PolicyAgreement.load().save()
        except Exception:
            pass

import json
from typing import Any, List
import re

from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe
from django.template.defaultfilters import capfirst
from django.utils import translation
from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from sorl.thumbnail import get_thumbnail
from django.core.exceptions import ValidationError


from config.utils import manual_formsets
from .models import *
from .validators import validate_geo


class PhotosInlineAdminFormSet(admin.helpers.InlineAdminFormSet):
    def inline_formset_data(self) -> str:
        """Change JSON for the Add another {{ ObjectPhoto }} button"""

        verbose_name = self.opts.verbose_name
        return json.dumps(
            {
                "name": "#%s" % self.formset.prefix,
                "options": {
                    "prefix": self.formset.prefix,
                    # "addText": "Добавить %(verbose_name)s"
                    "addText": "Добавить"
                    % {
                        "verbose_name": capfirst(verbose_name),
                    },
                    "deleteText": translation.gettext("Remove"),
                },
            }
        )


class PhoneForm(forms.ModelForm):
    phone = forms.CharField()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^[+]?\d{1,5}\s?[\(-]?\d{1,5}[\)-]?\s?(\d{1,5}-?){1,5}\d{1,5}$', phone):
            raise ValidationError('Введите корректный номер телефона')
        return phone


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 0
    form = PhoneForm


class InfoSocialForm(forms.ModelForm):
    link = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}), label = 'Ссылка')


class InfoSocialInline(admin.TabularInline):
    model = InfoSocial
    extra = 0
    form = InfoSocialForm


class InfoForm(forms.ModelForm):
    currency = forms.ChoiceField(choices=CURRENCIES, label=u'Валюта')
    address = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}),
                              label = u'Адрес')
    comment = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}),
                              label = u'Комментарий', required=False)
    latitude = forms.CharField(max_length=10, required=False, validators=[validate_geo],
                               label='Широта')
    longitude = forms.CharField(max_length=10, required=False, validators=[validate_geo],
                               label='Долгота')


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    inlines = [
        PhoneNumberInline,
        InfoSocialInline,
    ]

    fieldsets = [
            ('Информация',
            {
                "classes": [
                    "wide",
                    "extrapretty"
                ],
                'fields': [
                    'currency',
                    'address',
                    'comment',
                ]
            },),
            ('Геолокация',
            {
                "classes": [
                    "wide",
                    "extrapretty"
                ],
                'fields': [
                    'latitude',
                    'longitude',
                ]
            })
    ]

    list_display = [
        'change',
        'was_changed',
    ]
    form = InfoForm

    @admin.display(description='')
    def change(self, obj):
        return mark_safe(f'<b>Изменить</b>')

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            Info.load().save()
        except Exception:
            pass
    
    def has_add_permission(self, request, obj=None):
        return False
 
    def has_delete_permission(self, request, obj=None):
        return False

    def get_inline_formsets(self, request: HttpRequest, formsets: List[Any], inline_instances: List[Any], obj: Any | None = ...) -> List[Any]:
        """Change the Add button in inline formset"""
        inline_admin_formsets = super().get_inline_formsets(
            request, formsets, inline_instances, obj)
        return manual_formsets.improve_inline_formset(inline_admin_formsets)
    

class DishAdminFileWidget(AdminFileWidget):
    template_name = 'admin/widgets/dish_clearable_file_input.html'
    

class DishForm(forms.ModelForm):
    title = forms.CharField(max_length=256)
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}), required=False)
    photo = forms.ImageField(widget=DishAdminFileWidget, required=False)

    def clean_photo(self):
        file = self.cleaned_data.get('photo')
        if file is None:
            return
        if re.search(r'[а-яА-Я]', file.name):
            raise ValidationError(
                'Russian letters are not allowed'
            )
        return file


class DishesInline(admin.TabularInline):
    model = Dish
    extra = 0
    form = DishForm
    fields = ['title', 'description', 'photo', 'preview']
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.photo:
            img = get_thumbnail(obj.photo, '70x70', crop='center', quality=99)
            res = mark_safe(f'<img src="{img.url}">')
            return res

    preview.short_description = u''
    preview.allow_tags = True


class MealForm(forms.ModelForm):
    title = forms.CharField(max_length=256, help_text='Пример: завтрак')
    time = forms.CharField(widget=forms.TimeInput(attrs={'placeholder': '00:00', 'type': 'time'}))
    price = forms.DecimalField()


class MealInline(admin.TabularInline):
    model = Meal
    extra = 0
    fields = ['title', 'time', 'price']
    form = MealForm


@admin.register(FeedingInfo)
class FeedingInfoAdmin(admin.ModelAdmin):
    inlines = [
        MealInline,
        DishesInline,
    ]
    
    list_display = [
        'change',
        'was_changed',
    ]

    @admin.display(description='')
    def change(self, obj):
        return mark_safe(f'<b>Изменить</b>')

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            FeedingInfo.load().save()
        except Exception:
            pass
    
    def has_add_permission(self, request, obj=None):
        return False
 
    def has_delete_permission(self, request, obj=None):
        return False

    def get_inline_formsets(self, request: HttpRequest, formsets: List[Any], inline_instances: List[Any], obj: Any | None = ...) -> List[Any]:
        """Change the Add button in inline formset"""
        inline_admin_formsets = super().get_inline_formsets(
            request, formsets, inline_instances, obj)
        return manual_formsets.improve_inline_formset(inline_admin_formsets)
    

class RuleForm(forms.ModelForm):
    content = forms.CharField(max_length=80, widget=forms.Textarea(attrs={'cols': 80, 'rows': 3}), label = 'Содержание')

    class Meta:
        model = Rule
        exclude = ["created_at"]


class RuleInline(admin.TabularInline):
    model = Rule
    extra = 0
    form = RuleForm


@admin.register(RulesInfo)
class RulesAdmin(admin.ModelAdmin):
    inlines = [
        RuleInline,
    ]
    
    list_display = [
        'change',
        'was_changed',
    ]

    @admin.display(description='')
    def change(self, obj):
        return mark_safe(f'<b>Изменить</b>')

    @admin.display(description='')
    def rules_list(self, obj):
        queryset = Rule.objects.all()
        res = [rule.content for rule in queryset]
        return res

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            RulesInfo.load().save()
        except Exception:
            pass
    
    def has_add_permission(self, request, obj=None):
        return False
 
    def has_delete_permission(self, request, obj=None):
        return False

    def get_inline_formsets(self, request: HttpRequest, formsets: List[Any], inline_instances: List[Any], obj: Any | None = ...) -> List[Any]:
        """Change the Add button in inline formset"""
        inline_admin_formsets = super().get_inline_formsets(
            request, formsets, inline_instances, obj)
        return manual_formsets.improve_inline_formset(inline_admin_formsets)
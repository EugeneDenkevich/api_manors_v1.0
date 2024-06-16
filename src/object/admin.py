from typing import Any
import os
import re

from django.contrib import admin
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.core.exceptions import ValidationError
from django.urls import path, reverse

from config.utils import manual_formsets
from config.settings import STATIC_URL
from .models import *
from .admin_filters import *
from .logic import *


ICON_NEW_URL = os.path.join(STATIC_URL, 'admin', 'img', 'new.png')
ICON_YES_URL = os.path.join(STATIC_URL, 'admin', 'img', 'yes.png')
ICON_NO_URL = os.path.join(STATIC_URL, 'admin', 'img', 'no.png')
ICON_CLOSED_URL = os.path.join(STATIC_URL, 'admin', 'img', 'closed.png')
ICON_WIDTH = 13

EMPTY_VALUE = '---'


class PhotoObjectForm(forms.ModelForm):
    file = forms.ImageField(widget=AdminFileWidget)

    class Meta:
        model = PhotoObject
        fields = "__all__"
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if re.search(r'[а-яА-Я]', file.name):
            raise ValidationError(
                'Русские буквы в названии недопустимы'
            )
        return file


class PhotoObjectInline(admin.TabularInline):
    model = PhotoObject
    extra = 0
    readonly_fields = ['preview']
    fields = ['preview', 'file']
    form = PhotoObjectForm

    def preview(self, obj):
        if obj.file:
            img = get_thumbnail(obj.file, '70x70', crop='center', quality=99)
            res = mark_safe(f'<img src="{img.url}">')
            return res

    preview.short_description = u'Фото'
    preview.allow_tags = True


class FeatureForm(forms.ModelForm):
    class Meta:
        model = ObjectFeature
        fields = '__all__'


class ObjectFeaturestInline(admin.TabularInline):
    model = ObjectFeature
    extra = 0
    form = FeatureForm


class RoomsInline(admin.TabularInline):
    model = Room
    extra = 0


class BedsInline(admin.TabularInline):
    model = Bed
    extra = 0


class ObjectForm(forms.ModelForm):
    description_short = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 60, 'rows': 6}), label='Короткое описание')


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Описание объекта',
            {
                "classes": [
                    "wide",
                    "extrapretty"
                ],
                'fields': [
                    'title',
                    'pers_num',
                    'description_short',
                    'description_long',
                    'price_weekday',
                    'price_holiday',
                ]
            }
        )
    ]
    list_display = [
        'preview',
        'title_bold',
        'pers_num',
        'prices',
        'purchase',
    ]
    list_filter = [
        # IsReserved,
        # PriceFilter,
        PersNum,
    ]
    search_fields = ['title']
    search_help_text = 'Поиск по названию'
    inlines = [
        PhotoObjectInline,
        ObjectFeaturestInline,
        RoomsInline,
        BedsInline,
    ]
    list_display_links = ['preview', 'title_bold']
    form = ObjectForm

    @admin.display(description='Фото')
    def preview(self, obj):
        photo = obj.photos.all().first()
        if photo:
            img = get_thumbnail(photo.file, '70x70', crop='center', quality=99)
            res = mark_safe(f'<img src="{img.url}">')
            return res

    @admin.display(description='Цена р/в')
    def prices(self, obj):
        if obj.price_holiday:
            return f'{obj.price_weekday} / {obj.price_holiday}'
        else:
            return f'{obj.price_weekday} / {EMPTY_VALUE}'

    @admin.display(description='Заказы')
    def purchase(self, obj):
        if obj.purchases.all():
            purchases = obj.purchases.all()
            res = []
            for p in purchases:
                url = reverse(f"admin:object_purchase_change", args=(p.pk,))
                if p.stat == 'New':
                    res.append(
                        f'<b><a href="{url}">Заказ {p.pk}</b> <img src={ICON_NEW_URL} width={ICON_WIDTH}>')
                elif p.stat == 'Approved':
                    res.append(
                        f'<b><a href="{url}">Заказ {p.pk}</b> <img src={ICON_YES_URL} width={ICON_WIDTH}>')
                else:
                    res.append(f'<b><a href="{url}">Заказ {p.pk}</b>')
                    print('Something is wrong with purchase.stat '
                          '- look at the object.admin.ObjectAdmin '
                          'in "purchase" method')
            return mark_safe('<br>'.join(res))

    @admin.display(description='Название')
    def title_bold(self, obj):
        return mark_safe(f'<b>{obj.title}</b>')

    def get_inline_formsets(self, request, formsets, inline_instances, obj: Any | None = ...):
        inline_admin_formsets = super().get_inline_formsets(
            request, formsets, inline_instances, obj)
        return manual_formsets.improve_inline_formset(inline_admin_formsets)
    
    def change_view(self, request: HttpRequest, object_id: str = None, form_url: str = '',
                    extra_context = {}):
        extra_context['model_title'] = self.model._meta.verbose_name
        return super().change_view(request, object_id, form_url, extra_context)


class PurchaseAdminObjectFrom(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 60, 'rows': 6}), label='Адрес',
        required=False)
    pets = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 60, 'rows': 6}), label='Инфо о животных',
        required=False)
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 60, 'rows': 6}), label='Комментарий закзачика',
        required=False)

    class Meta:
        model = Purchase
        exclude = [
            'status',
            'stat',
            'is_finished',
        ]

    def clean_object(self):
        house = self.cleaned_data.get('object')
        if house is None:
            raise ValidationError('Добавьте домик')
        return house

    def clean_desired_departure(self):
        desired_departure = self.cleaned_data['desired_departure']
        desired_arrival = self.cleaned_data['desired_arrival']
        if desired_departure < desired_arrival:
            raise ValidationError('Дата выезда должна быть раньше даты заезда')
        return desired_departure


class PurchaseAdminNotObjectFrom(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = [
            'was_object',
            'fio',
            'passport_country',
            'address',
            'phone_number',
            'email',
            'telegram',
            'desired_arrival',
            'desired_departure',
            'count_adult',
            'count_kids',
            'pets',
            'comment',
        ]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    change_form_template = "admin/model_change_form_purchase.html"
    form = PurchaseAdminObjectFrom
    list_display = [
        'title',
        'arrival',
        'house',
        'status_manual',
    ]

    list_filter = [
        # EarliestDate,
        'stat'
    ]

    @admin.display(description='Статус')
    def status_manual(self, object):
        if object.stat == 'New':
            return mark_safe(f"<img src={ICON_NEW_URL} width={ICON_WIDTH}> Новая")
        elif object.stat == 'Approved':
            return mark_safe(f"<img src={ICON_YES_URL} width={ICON_WIDTH}> Одобрена")
        elif object.stat == 'Denied':
            return mark_safe(f"<img src={ICON_NO_URL} width={ICON_WIDTH}> Отклонена")
        elif object.stat == 'Closed':
            return mark_safe(f"<img src={ICON_CLOSED_URL} width={ICON_WIDTH}> Завершена")

    @admin.display(description='Заявка')
    def title(self, object):
        return f'Заявка #{object.pk}'

    @admin.display(description='Даты: Заезд / Выезд')
    def arrival(self, object):
        return mark_safe(f'<b>{object.desired_arrival.strftime("%d.%m.%y")}</b> / <b>{object.desired_departure.strftime("%d.%m.%y")}</b>')

    @admin.display(description='Домик')
    def house(self, object):
        if object.object != None:
            pk = object.object.pk
            url = reverse("admin:object_object_change", args=(pk,))
            return mark_safe(f'<b><a href="{url}">{object.object.title}</b>')
        else:
            try:
                pk = object.was_object.pk
                url = reverse("admin:object_object_change", args=(pk,))
                return mark_safe(f'<a href="{url}">{object.was_object.title}')
            except:
                return

    def get_urls(self):
        urls = super(PurchaseAdmin, self).get_urls()
        custom_urls = [path('change-purchase', self.admin_site.admin_view(self.change_purchase_status), name='change_purchase_status'),
                       path('change-purchase_finished', self.admin_site.admin_view(
                           self.change_purchase_is_finished), name='change_purchase_is_finished'),
                       path('change_purchase_denied', self.admin_site.admin_view(self.change_purchase_denied), name='change_purchase_denied'),]
        new_urls = custom_urls + urls
        return new_urls

    def get_form(self, request, obj=None, **kwargs):
        if obj != None:
            if obj.object is not None:
                kwargs["form"] = PurchaseAdminObjectFrom
            else:
                kwargs["form"] = PurchaseAdminNotObjectFrom
            self.__dict__['current_purchase'] = obj
        else:
            pass
        return super().get_form(request, obj, **kwargs)

    def change_purchase_status(self, request):
        purchase = self.__dict__.get('current_purchase')
        change_status(purchase)
        return redirect(request.META.get('HTTP_REFERER'))

    def change_purchase_is_finished(self, request):
        purchase = self.__dict__.get('current_purchase')
        if not purchase.is_finished:
            finish_purchase(purchase)
        return redirect(request.META.get('HTTP_REFERER'))

    def change_purchase_denied(self, request):
        purchase = self.__dict__.get('current_purchase')
        if purchase.stat == 'New':
            deny_purchase(purchase)
        return redirect(request.META.get('HTTP_REFERER'))
    
    def change_view(self, request: HttpRequest, object_id: str = None, form_url: str = '',
                    extra_context = {}):
        extra_context['model_title'] = self.model._meta.verbose_name
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.empty_value_display = EMPTY_VALUE
admin.site.site_header = u'Заповедный остров. Администрирование'
admin.site.site_title = u'Заповедный остров'
admin.site.index_title = u'Панель управления'

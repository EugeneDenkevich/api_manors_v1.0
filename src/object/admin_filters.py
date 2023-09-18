from django.contrib import admin


class PriceFilter(admin.SimpleListFilter):
    title = 'Цена'
    parameter_name = 'price_weekday'

    def lookups(self, request, model_admin):
        return [
            ("desc", 'По убыванию'),
            ('asc', 'По возрастанию'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'desc':
            return queryset.all().order_by("-price_weekday")
        if self.value() == 'asc':
            return queryset.all().order_by("price_weekday")


class PersNum(admin.SimpleListFilter):
    title = 'Вместимость'
    parameter_name = 'pers_num'

    def lookups(self, request, model_admin):
        return [
            ("desc", 'По убыванию'),
            ('asc', 'По возрастанию'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'desc':
            return queryset.all().order_by('-pers_num')
        if self.value() == 'asc':
            return queryset.all().order_by('pers_num')
        

class IsReserved(admin.SimpleListFilter):
    title = 'По заказам'
    parameter_name = 'is_reserved'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Свободные'),
            ('no', 'Занятые'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_reserved=0)
        if self.value() == 'no':
            return queryset.filter(is_reserved=1)
        

class EarliestDate(admin.SimpleListFilter):
    title = 'По завершению'
    parameter_name = 'desired_departure'

    def lookups(self, request, model_admin):
        return [
            ('asc', 'От ранних'),
            ('desc', 'От поздних'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'asc':
            return queryset.all().order_by('desired_departure')
        if self.value() == 'desc':
            return queryset.all().order_by('-desired_departure')

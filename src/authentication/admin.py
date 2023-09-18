from typing import Any, Optional
from django.contrib import admin
from django.contrib.auth.models import Group
from django.http.request import HttpRequest
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    PasswordChangeView,
)

from authentication import models
from authentication import forms as auth_forms


@admin.register(models.BaseUser)
class UserAdmin(admin.ModelAdmin):
    change_form_template = "admin/model_change_form_authentication.html"
    form = auth_forms.BaseUserFormChange
    add_form = auth_forms.BaseUserFormCreate
    superuser_form = auth_forms.SuperUserFormChange
    list_display = [
        'email',
        'was_changed',
    ]

    def has_add_permission(self, request: HttpRequest) -> bool:
        user = request.user
        if hasattr(user, 'owner'):
            return False
        else:
            return True

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        user = request.user
        if hasattr(user, 'owner'):
            return False
        else:
            return True

    def get_form(self, request, obj=None, **kwargs):
        """
        Using special for creating new user
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        elif not hasattr(obj, 'owner'):
            defaults['form'] = self.superuser_form
        defaults.update(kwargs)

        return super().get_form(request, obj, **defaults)

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()
        custom_urls = [path('password-change/',
                            PasswordChangeView.as_view(success_url=reverse_lazy('admin:password_change_done')),
                            name='password_change')]
        return custom_urls + urls


admin.site.unregister(Group)

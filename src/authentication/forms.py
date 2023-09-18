from django.forms import (
    ModelForm,
    CharField,
    PasswordInput,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import password_validation

from authentication import models


class BaseUserFormCreate(ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    first_name = CharField(label=_('First name'))
    last_name = CharField(label=_('Last name'))
    password1 = CharField(
        label=_("Password"),
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = models.BaseUser
        fields = [
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = ''
        self.fields['password1'].initial = ''

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user: models.BaseUser = super().save(commit=False)
        user.is_staff = True
        user.is_admin = True
        user.set_password(self.cleaned_data.get('password1'))
        user.save()
        if (self.cleaned_data.get('first_name') and
                self.cleaned_data.get('last_name')):
            owner = models.Owner.objects.create(
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                user=user
            )
            owner.save()

        return user


class BaseUserFormChange(ModelForm):
    first_name = CharField(label='Имя')
    last_name = CharField(label='Фамилия')

    class Meta:
        model = models.BaseUser
        fields = [
            'email',
            'first_name',
            'last_name',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.owner.first_name
        self.fields['last_name'].initial = self.instance.owner.last_name

    def save(self, commit=True):
        user: models.BaseUser = super().save(commit=False)
        user.save()
        if (self.cleaned_data.get('first_name') and
                self.cleaned_data.get('last_name')):
            owner = models.Owner.objects.get(
                pk=user.owner.pk
            )
            owner.first_name = self.cleaned_data.get('first_name')
            owner.last_name = self.cleaned_data.get('last_name')
            owner.save()

        return user


class SuperUserFormChange(ModelForm):

    password = CharField(widget=PasswordInput, label=_('Password'))
    password2 = CharField(widget=PasswordInput, label=_('Password confirmation'))

    class Meta:
        model = models.BaseUser
        fields = [
            'email',
            'password',
            'password2',
            'is_admin',
            'is_staff',
            'is_active'
        ]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError('Passwords don\'t match')

        return password

    def save(self, commit=True):
        user: models.BaseUser = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.save()

        return user

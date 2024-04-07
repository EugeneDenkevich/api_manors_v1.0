from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):

    def __create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError("Users must have and email.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self.__create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True")

        return self.__create_user(email, password, **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Адрес электронной почты", unique=True)
    was_changed = models.DateField(auto_now=True, verbose_name="Изменено")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Owner(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user = models.OneToOneField(
        to=BaseUser,
        on_delete=models.CASCADE,
        related_name="owner",
    )

    class Meta:
        verbose_name = "owner"
        verbose_name_plural = "owner"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TelegramIdUser(models.Model):
    telegram_id = models.CharField(max_length=120)

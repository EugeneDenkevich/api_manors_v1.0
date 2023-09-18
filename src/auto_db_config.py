import os
from dotenv import load_dotenv, find_dotenv

import django


# Set django settings.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from django.conf import settings

load_dotenv(find_dotenv())

if not settings.configured:
    django.setup()


from authentication.models import BaseUser


def create_admin() -> None:
    """
    Creates new admin
    """
    BaseUser.objects.create_superuser(
        email=os.environ.get('DJANGO_ADMIN_EMAIL'),
        password=os.environ.get('DJANGO_ADMIN_PASS')
    )


# Create new admin and exception if he already exists.
if __name__ == "__main__":
    try:
        create_admin()
        print('Admin was created.')
    except django.db.utils.IntegrityError:
        print('Admin already exists.')
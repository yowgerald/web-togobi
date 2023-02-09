from django.contrib.auth.models import User
from faker import Faker
from django.utils import timezone
from togobi.models import Location
from togobi.models import UserDetail
import random

fake = Faker()

def user_seeder(default_username = None, default_password = None):
    user = User(
        username = 
            default_username if default_username is not None 
            else fake.user_name(),
        first_name = fake.first_name(),
        last_name = fake.last_name(),
        email = fake.email(),
        is_staff = False,
        is_active = True,
        is_superuser = False,
        date_joined = timezone.now()
    )

    password = default_password if default_password is not None else 'password'
    user.set_password(password)
    user.save()

    location_ids = Location.objects.values_list('id', flat=True)
    location = Location.objects.get(pk=random.choice(location_ids))
    user_detail = UserDetail(
        updated_at = timezone.now(),
        location = location,
        user = user
    )
    user_detail.save()

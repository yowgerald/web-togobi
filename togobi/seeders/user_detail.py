from django.contrib.auth.models import User
from django.utils import timezone
from togobi.models import Location
from togobi.models import UserDetail
from payments.models import Plan
import random
from django.conf import settings

def user_detail_seeder():
    users = User.objects.all()
    
    for user in users:
        user_detail = UserDetail.objects.filter(user=user)
        if user_detail.exists():
            continue

        location_ids = Location.objects.values_list('id', flat=True)
        location = Location.objects.get(pk=random.choice(location_ids))

        plan_ids = Plan.objects.values_list('id', flat=True)
        plan = Plan.objects.get(pk=random.choice(plan_ids))

        user_detail = UserDetail(
            updated_at = timezone.now(),
            location = location,
            plan=plan,
            user = user
        )
        user_detail.save()

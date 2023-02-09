from django.core.management.base import BaseCommand
from accounts.seeders import *
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('seeding users...')
        # default user
        user_seeder(settings.DEV_USER, settings.DEV_PASSWORD)
        for i in range(10):
            #random users
            user_seeder()
        self.stdout.write('done.')



from django.core.management.base import BaseCommand
from togobi.seeders import *
import os
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        if settings.DEBUG:
            self.stdout.write('cleaning database...')
            os.system("python manage.py flush")
            self.stdout.write('done.')
        # Location
        self.stdout.write('seeding locations...')
        for i in range(10):
            location_seeder()
        self.stdout.write('done.')

        # TODO: plan seeder

        # User / UserDetails
        self.stdout.write('seeding Users...')
        # default user
        user_seeder(settings.DEV_USER, settings.DEV_PASSWORD)
        for i in range(10):
            #random users
            user_seeder()
        self.stdout.write('done.')



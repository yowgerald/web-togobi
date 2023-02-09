from django.core.management.base import BaseCommand
from togobi.seeders import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Location
        self.stdout.write('seeding locations...')
        for i in range(10):
            location_seeder()
        self.stdout.write('done.')

        # UserDetails
        self.stdout.write('seeding User Details...')
        user_detail_seeder()
        self.stdout.write('done.')



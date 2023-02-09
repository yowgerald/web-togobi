from django.core.management.base import BaseCommand
from payments.seeders import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('seeding plans...')
        payment_seeder()
        self.stdout.write('done.')



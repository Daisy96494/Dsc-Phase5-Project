import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from entrypoint.models import LocationData


class Command(BaseCommand):
    help = "Import location data from a csv file into a database table"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to the CSV file")
    
    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                LocationData.objects.create(
                    location=row['city'],
                    country=row['country'],
                    iso3=row['iso3'],
                    latitude=row['lat'],
                    longitude=row['lng']
                )
        self.stdout.write(self.style.SUCCESS("Successfully imported CSV data into database."))

        
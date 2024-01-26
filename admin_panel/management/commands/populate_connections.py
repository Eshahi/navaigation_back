# your_app/management/commands/populate_connections.py
from django.core.management.base import BaseCommand
from admin_panel.graph_utils import rebuild_graph  # Update the import path as necessary


class Command(BaseCommand):
    help = 'Populate the Connection table with connections based on the nearest rooms'

    def handle(self, *args, **options):
        self.stdout.write("Starting to populate connections...")
        rebuild_graph()
        self.stdout.write(self.style.SUCCESS('Successfully populated connections between rooms'))

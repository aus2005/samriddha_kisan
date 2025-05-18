from django.core.management.base import BaseCommand
from market_prices.utils import scrape_and_save_table

class Command(BaseCommand):
    help = 'Scrape prices and save to DB'

    def handle(self, *args, **kwargs):
        scrape_and_save_table()
        self.stdout.write("Scraped and saved prices.")
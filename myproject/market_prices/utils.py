import requests
from bs4 import BeautifulSoup
from .models import PriceTable
from datetime import date

def scrape_and_save_table():
    url = "https://kalimatimarket.gov.np"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch webpage")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.select_one("table")  # Grabs the first table
    if not table:
        print("No table found.")
        return

    PriceTable.objects.update_or_create(
        date=date.today(),
        defaults={"html": str(table)}
    )
    print("Table scraped and saved.")
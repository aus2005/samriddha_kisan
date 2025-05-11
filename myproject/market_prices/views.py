from django.shortcuts import render, redirect
from .models import PriceTable
from .utils import scrape_and_save_table  
from datetime import date

def today_table(request):
    try:
        price_table = PriceTable.objects.get(date=date.today())
        table_html = price_table.html
    except PriceTable.DoesNotExist:
        table_html = "<p>आजको लागि तालिका उपलब्ध छैन।</p>"

    return render(request, "market_prices/today_table.html", {"table_html": table_html})

def update_prices(request):
    if request.method == "POST":
        scrape_and_save_table()
    return redirect("today_table")
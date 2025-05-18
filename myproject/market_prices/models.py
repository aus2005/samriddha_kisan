from django.db import models

# Create your models here.
class PriceTable(models.Model):
    html = models.TextField()
    date = models.DateField(unique=True)

    def __str__(self):
        return f"Prices for {self.date}"
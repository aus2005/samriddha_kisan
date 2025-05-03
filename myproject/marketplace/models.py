from django.db import models

from django.conf import settings

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('grain', 'Grain'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
       
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)  # % off
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

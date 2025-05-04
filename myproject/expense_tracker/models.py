from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'आय'),
        ('expense', 'खर्च'),
    )

    CATEGORY_CHOICES = (
        ('crop_sales', 'बाली बिक्री'),
        ('equipment_purchase', 'उपकरण खरिद'),
        ('fertilizer', 'मल/बिउ खरिद'),
        ('transport', 'यातायात'),
        ('labor', 'श्रमिक खर्च'),
        ('loan_payment', 'ऋण भुक्तानी'),
        ('misc', 'अन्य'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name="प्रयोगकर्ता")

    date = models.DateField(auto_now_add=True, verbose_name="मिति")
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES, verbose_name="प्रकार")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="श्रेणी")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="रकम (रु.)")
    description = models.TextField(blank=True, null=True, verbose_name="विवरण")

    def __str__(self):
        nepali_type = dict(self.TRANSACTION_TYPES).get(self.type, self.type)
        return f"{nepali_type} - रु. {self.amount} ({self.date})"

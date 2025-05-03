from django.shortcuts import render
from django.conf import settings
from .models import Product

def marketplace(request):
    category = request.GET.get('category') 
    
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    
    categories = Product.CATEGORY_CHOICES

    return render(request, 'marketplace.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'MEDIA_URL': settings.MEDIA_URL  
    })

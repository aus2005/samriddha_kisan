from django.shortcuts import render
from django.conf import settings
from .models import Product
from django.contrib.auth.decorators import login_required
from item.models import Item
def marketplace(request):
    category = request.GET.get('category') 
    
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    
    categories = Product.CATEGORY_CHOICES

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'MEDIA_URL': settings.MEDIA_URL  
    })


@login_required
def index(request):
  items=Item.objects.filter(created_by=request.user)
  return render(request,'index.html',{
    'items':items,
  })

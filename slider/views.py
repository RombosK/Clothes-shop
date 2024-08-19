from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Slider
from store.models import Product

def home(request):
    slider_list = Slider.objects.all()
    most_popular_products = Product.objects.filter(is_popular=True)  # Пример фильтрации популярных товаров
    context = {
        'slider_list': slider_list,
        'most_popular_products': most_popular_products
    }
    return render(request, 'home.html', context)

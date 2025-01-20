from django.shortcuts import render, get_object_or_404
from .models import Category, Furniture

def shop(request):
    furnitures = Furniture.objects.all()
    return render(request, 'shop/shop.html', {'furnitures': furnitures})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})

def furniture_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    furniture = Furniture.objects.filter(category=category)
    return render(request, 'shop/furniture_list.html', {'category': category, 'furniture': furniture})

def furniture_detail(request, product_id):
    furniture = get_object_or_404(Furniture, pk=product_id)
    return render(request, 'shop/detail.html', {'furniture': furniture})




from django.contrib import admin

from .models import Category, Furniture, FurnitureDetail

admin.site.register(Category)
admin.site.register(Furniture)
admin.site.register(FurnitureDetail)

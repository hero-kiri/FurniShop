from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('shop/<int:product_id>/', views.furniture_detail, name='product_detail'),
]
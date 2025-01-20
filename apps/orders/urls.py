from django.urls import path
from . import views
urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order_history/', views.order_history_view, name='order_history'),
    path('add_to_cart/<int:furniture_id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:item_id>', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>', views.decrease_quantity, name='decrease_quantity'),
    path('thankyou/', views.thankyou_view, name='thankyou'),
]
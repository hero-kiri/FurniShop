from django.db import models
from apps.users.models import CustomUser
from apps.shop.models import Furniture
import random
from django.core.mail import send_mail
from django.conf import settings


class Order(models.Model):
    
    ORDER_STATUS = (
        ('Новый', 'Новый'),
        ('В обработке', 'В обработке'),
        ('Отправлен', 'Отправлен'),
        ('Доставлен', 'Доставлен'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100)
    address = models.TextField()
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    order_notes = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Новый')
    
    def send_order_confirmation_email(self):
        products = '\n'.join([f"{item.furniture.name} (x{item.quantity})" for item in self.items.all()])
        subject = f"Подтверждение заказа - {self.id}"
        message = f"Уважаемый(ая) {self.first_name} {self.last_name},\n\n" \
                  f"Спасибо за ваш заказ!\n\n" \
                  f"Детали заказа:\n" \
                  f"ID заказа: {self.id}\n" \
                  f"Общая стоимость: ${self.total_price}\n\n" \
                  f"Товары:\n" \
                  f"{products}\n\n" \
                  f"Мы уведомим вас, как только ваш заказ будет отправлен.\n\n" \
                  f"С уважением,\n" \
                  f"Команда FurniYeldos"
        
        recipient_list = [self.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    
    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_price(self):
        return self.furniture.price * self.quantity
    
    def __str__(self):
        return f"{self.furniture.name} (x{self.quantity})"

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def total_price(self):
        if self.coupon:
            discount = self.coupon.discount
            total_price = sum(item.total_price for item in self.items.all())
            return total_price - (total_price * discount / 100)
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_intermediate_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def total_price(self):
        return self.furniture.price * self.quantity
    
    def __str__(self):
        return f"{self.furniture.name} (x{self.quantity}) {self.cart.user.first_name}"
    

class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    
    def __str__(self):
        return self.code
    


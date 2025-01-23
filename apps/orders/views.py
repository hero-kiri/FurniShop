from django.shortcuts import render, redirect, get_object_or_404
from .models import Furniture, Order, OrderItem, Cart, CartItem, PromoCode
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if created:
        messages.success(request, 'Вы успешно создали корзину') 

    cart_items = CartItem.objects.filter(cart=cart)

    context = {
        'cart_items': cart_items,
        'cart': cart,
    }
    return render(request, 'orders/cart.html', context=context)

@login_required
def add_to_cart(request, furniture_id):
    furniture = get_object_or_404(Furniture, id=furniture_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, furniture=furniture)
    cart_item.quantity += 1
    cart_item.save()
    if created:
        messages.success(request, 'Товар успешно добавлен в корзину')
    else:
        messages.success(request, 'Количество товара в корзине увеличено на 1')
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def thankyou_view(request):
    return render(request, 'orders/thankyou.html')

@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST['c_fname'],
            last_name=request.POST['c_lname'],
            company_name=request.POST.get('c_companyname', ''),
            country=request.POST['c_country'],
            address=request.POST['c_address'],
            state=request.POST['c_state_country'],
            postal_code=request.POST['c_postal_zip'],
            email=request.POST['c_email_address'],
            phone=request.POST['c_phone'],
            order_notes=request.POST.get('c_order_notes', ''),
            total_price=cart.total_price
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order, 
                furniture=item.furniture, 
                quantity=item.quantity, 
                price=item.total_price
            )
        cart.items.all().delete()
        messages.success(request, 'Заказ успешно создан')
        return redirect('thankyou')
    
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'orders/checkout.html', context=context)

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def apply_promo_code(request, redirect_url):
    if request.method == 'POST':
        code = request.POST.get('promo_code')
        promo_code = PromoCode.objects.filter(code=code).first()
        print(promo_code, code)
        if promo_code:
            if promo_code.is_active:
                if promo_code.expired_at and promo_code.expired_at < timezone.now():
                    messages.error(request, 'Промокод просрочен')
                else:
                    cart, created = Cart.objects.get_or_create(user=request.user)
                    cart.coupon = promo_code
                    cart.save()
                    messages.success(request, 'Промокод успешно применен')
            else:
                messages.error(request, 'Промокод не активен')
        else:
            messages.error(request, 'Промокод не найден')
    return redirect(redirect_url)

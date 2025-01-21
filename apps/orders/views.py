from django.shortcuts import render, redirect, get_object_or_404
from .models import Furniture, Order, OrderItem, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def cart_view(request):
    """
    get_or_create() возвращает кортеж с объектом и булевым значением, указывающим, был ли объект создан или нет.
    a = (Cart, False)
    cart, created = a
    """
    # Получаем корзину пользователя или создаем новую 
    cart, created = Cart.objects.get_or_create(user=request.user)
    if created:
        messages.success(request, 'Вы успешно создали корзину') 

    # Получаем все товары в корзине и общую стоимость
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = cart.total_price()

    context = {
        'cart_items': cart_items, 
        'total_price': total_price
        }
    return render(request, 'orders/cart.html', context=context)


@login_required
def add_to_cart(request, furniture_id):
    """
    Добавление товара в корзину пользователя
    furniture_id - id товара
    """
    # Получаем товар по id или возвращаем 404 если товар не найден
    furniture = get_object_or_404(Furniture, id=furniture_id)
    
    # Получаем корзину пользователя или создаем новую
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Получаем товар в корзине или создаем новый товар в корзине и увеличиваем количество на 1
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
    # Получаем товар в корзине или возвращаем 404 если товар не найден
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')



@login_required
def increase_quantity(request, item_id):
    # Получаем товар в корзине или возвращаем 404 если товар не найден
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    # Увеличиваем количество товара на 1
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
    return render(request, 'orders/checkout.html')


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
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
            total_price=sum(item.total_price() for item in cart.items.all())
        )
        for item in cart.items.all():
            OrderItem.objects.create(order=order, furniture=item.Furniture, quantity=item.quantity, price=item.total_price())
        cart.items.all().delete()
        return redirect('thankyou')
    return render(request, 'checkout.html', {'cart': cart})


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


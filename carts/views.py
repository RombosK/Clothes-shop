from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation


def _cart_id(request):
    """
    Получение корзины по ключу session_key, присутствующему в сессии
    :param request:
    :return: Содержание корзины по определенному ключу сессии
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    """
    Добавляет конкретный товар в корзину по его идентификатору и вариациям (цвет, размер и т. д.)
    если пользователь аутентифицирован и нет.
    :param request:
    :param product_id: id товара, который мы хотим добавить в корзину
    :return: перенаправление пользователя на страницу "Корзина".
    """
    current_user = request.user
    product = Product.objects.get(id=product_id)  # get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            existing_variation_list = [list(item.variations.all()) for item in cart_item]
            item_id_list = [item.id for item in cart_item]

            if product_variation in existing_variation_list:
                # increase the cart item quantity
                item_index = existing_variation_list.index(product_variation)
                item = CartItem.objects.get(product=product, id=item_id_list[item_index])
                item.quantity += 1
                item.save()
            else:
                # create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    # Если пользователь не прошел аутентификацию
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # получаем корзину, используя cart_id в сессии
        except ObjectDoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            existing_variation_list = [list(item.variations.all()) for item in cart_item]
            item_id_list = [item.id for item in cart_item]

            if product_variation in existing_variation_list:
                # increase the cart item quantity
                item_index = existing_variation_list.index(product_variation)
                item = CartItem.objects.get(product=product, id=item_id_list[item_index])
                item.quantity += 1
                item.save()
            else:
                # create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    """
    Нажатие кнопки "минус" уменьшает количество товара на единицу.
    :param cart_item_id:
    :param request:
    :param product_id:
    :return: Отображение страницы корзины с новым количеством товара
    """
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    """
   Нажатие кнопки удаления удаляет товар из корзины.
    :param cart_item_id:
    :param request:
    :param product_id:
    :return: Рендеринг страницы корзины с новым списком товаров
    """
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart_page(request, total=0, quantity=0, cart_items=None, discount=0, grand_total=0):
    """
    Эта функция выводит страницу 'Корзина' и вычисляет общую сумму, количество, скидку и общую сумму.
    :param request:
    :param total: Сумма без скидки на текущий момент
    :param quantity: Количество товара в текущий момент времени
    :param cart_items: Товары в корзине
    :param discount: Сумма скидки
    :param grand_total: Сумма с учетом скидки
    :return: Вывод страницы 'корзина'
    """
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        if total < 5000:
            discount = round(total * 0.03)
        else:
            discount = round(total * 0.07)
        grand_total = total - discount
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'discount': discount,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None, discount=0, grand_total=0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        if total < 5000:
            discount = round(total * 0.03)
        else:
            discount = round(total * 0.07)
        grand_total = total - discount
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'discount': discount,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)

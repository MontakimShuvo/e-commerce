from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product

from .models import Cart, CartItem
from .utils import get_session_key

# Create your views here.


def add_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    try:
        cart = Cart.objects.get(session_key=get_session_key(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_key=get_session_key(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
    except Cart.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, user=request.user)

    cart_item.quantity += 1
    cart_item.save()
    
    url = request.META.get("HTTP_REFERER")
    return redirect(url)

def remove_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            cart = Cart.objects.get(session_key=get_session_key(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    url = request.META.get("HTTP_REFERER")
    return redirect(url)

def cart_detail(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, cart__isnull=True)
        else:
            cart = Cart.objects.get(session_key=get_session_key(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True).select_related('product')
        for cart_item in cart_items:
            total += (cart_item.product.discount_price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "grand_total": total + settings.DELIVERY_CHARGE,
    }
    return render(request, "carts/cart.html", context)

   
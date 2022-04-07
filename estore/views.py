from django.shortcuts import redirect, render, get_object_or_404
from estore.models import Category, Product, Cart
import decimal


def home(request):
    categories = Category.objects.filter()[:3]
    products = Product.objects.filter()[:8]
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'estore/index.html', context)


def category_products(request, url_slug):
    category = get_object_or_404(Category, url_slug=url_slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'estore/category_products.html', context)


def cart(request):
    cart_products = Cart.objects.all()

    amount = cart_total()
    shipping_amount = decimal.Decimal(0)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount
    }
    return render(request, 'estore/cart.html', context)


def cart_total():
    amount = decimal.Decimal(0)
    cart_items = [item for item in Cart.objects.all()]
    if cart_items:
        for item in cart_items:
            temp_amount = (item.quantity * item.product.price)
            amount += temp_amount

    return amount


def add_to_cart(request):
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    item_already_in_cart = Cart.objects.filter(product=product_id)
    if item_already_in_cart:
        cart_item = get_object_or_404(Cart, product=product_id)
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart(product=product).save()

    return redirect('estore:cart')


def remove_from_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
    return redirect('estore:cart')


def increment_cart(request, cart_id):
    if request.method == 'GET':
        cart_item = get_object_or_404(Cart, id=cart_id)
        cart_item.quantity += 1
        cart_item.save()        
    return redirect('estore:cart')


def decrement_cart(request, cart_id):
    if request.method == 'GET':
        cart_item = get_object_or_404(Cart, id=cart_id)
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
    return redirect('estore:cart')
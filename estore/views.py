from django.shortcuts import redirect, render, get_object_or_404
from estore.models import Category, Product, Cart
import decimal
import base64
import requests
from requests.structures import CaseInsensitiveDict
import json
from datetime import datetime

headers = CaseInsensitiveDict()
headers['accept'] = 'application/json'
headers['Content-Type'] = 'application/json'
tokens = 'e5f1fdd8-de74-4d38-a66b-e094626d9014:bdcfe703-b344-4f23-87c0-cc34284b9330'
encoded = base64.b64encode(tokens.encode('ascii'))
headers['Authorization'] = 'Basic ' + encoded.decode('utf-8')

def verify(card_token, name, lastFour, expiration):
    #card_token = '9122c6a1-ea32-4238-8d7f-13bb44565ae8'

    url = "https://sandbox-api.marqeta.com/v3/cards/" + card_token

    response = requests.get(url, headers=headers)

    res = json.loads(response.text)
    if lastFour == res['last_four'] and expiration == res['expiration'] and name == res['fulfillment']['card_personalization']['text']['name_line_1']['value']:
        return True
    else:
        return False


def getCardToken(pan, name, lastFour, expiration):

    url = "https://sandbox-api.marqeta.com/v3/cards/getbypan"

    data = """
    {{
        "pan": "{0}"
    }}
    """

    temp = data.format(pan)

    resp = requests.post(url, headers=headers, data=temp)

    if resp.status_code == 200:
        res = json.loads(resp.text)
        if verify(res['card_token'], name, lastFour, expiration):
            return True, res['card_token']
    
    return False, ""

def transaction(pan, name, lastFour, expiration, amount):
    url = "https://sandbox-api.marqeta.com/v3/simulate/authorization"

    headers = CaseInsensitiveDict()
    headers['accept'] = 'application/json'
    headers['Content-Type'] = 'application/json'
    encoded = base64.b64encode('e5f1fdd8-de74-4d38-a66b-e094626d9014:bdcfe703-b344-4f23-87c0-cc34284b9330'.encode('ascii'))
    headers['Authorization'] = 'Basic ' + encoded.decode('utf-8')

    mid = '123456890'
    #card_token = '9122c6a1-ea32-4238-8d7f-13bb44565ae8'
    status, card_token = getCardToken(pan, name, lastFour, expiration)
    if status:
        data = """
        {{
            "amount": "{0}", 
            "mid": "{1}",
            "card_token": "{2}",
            "webhook": {{
                "endpoint": "**URL FOR RECEIVING NOTIFICATIONS**",
                "username": "**MY USER NAME**",
                "password": "**MY PASSWORD**"
            }}
        }}
        """

        temp = data.format(amount, mid, card_token)

        resp = requests.post(url, headers=headers, data=temp)

        if resp.status_code == 202:
            return True, resp.status_code
        else:
            return False, resp.status_code
    else:
        return False, ""

def checkout(request):
    if request.method == 'POST':
        pan = request.POST.get("pan")
        name = request.POST.get("name")
        lastFour = request.POST.get("lastFour")
        expiration =  request.POST.get("expiration")
        amount = request.POST.get("amount")

        isSuccess, statusCode = transaction(pan, name, lastFour, expiration, amount)

        context = {
            'isSuccess': isSuccess,
            'status_code': statusCode,
            'date': datetime.now().strftime("%A, %B %d, %Y"),
            'name': name,
            'pan': pan,
            'cart_total': amount
        }

        if isSuccess:
            context['message'] = 'Your transaction was successfully completed!'
            return render(request, 'estore/invoice.html', context)
        else:
            context['message'] = 'Your transaction could not be completed!'
            context['lastFour'] = lastFour
            context['expiration'] = expiration
            return render(request, 'estore/checkout.html', context)

        # pan = 1111115384669537

    context = {
        'cart_total': cart_total(),
        'isSuccess': True
    }

    return render(request, 'estore/checkout.html', context)

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
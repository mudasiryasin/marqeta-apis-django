from django.shortcuts import render
from django.http import HttpResponse
from marqeta import Client

base_url = "https://sandbox-api.marqeta.com/v3/"
application_token = "e5f1fdd8-de74-4d38-a66b-e094626d9014"
access_token = "bdcfe703-b344-4f23-87c0-cc34284b9330"
timeout = 60 # seconds

client = Client(base_url, application_token, access_token, timeout)

def index(request):
    return render(request, 'index.html')
    
def dashboard(request):
    return render(request, 'dashboard.html')

def shop(request):
    if request.method == 'POST':
        rate = request.POST.get("rate")
        quantity = request.POST.get("quantity")
        totalAmount = rate * quantity
        return render(request,'shop.html')

    cards = getCards()
    
    return render(request, 'shop.html', {"cards": cards})

def createUser(request):
    if request.method == 'POST':
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postalCode = request.POST.get("postalCode")
        country = request.POST.get("country")
        phone = request.POST.get("phone")
        dateOfBirth = request.POST.get("dateOfBirth")
        password = request.POST.get("password")
        #parentToken  = request.POST.get("lastName")
        #company = request.POST.get("lastName")
        #identifications = request.POST.get("lastName")

        data = {
            'first_name': firstName,
            'last_name': lastName,
            'gender': gender,
            'email': email,
            'address1': address,
            'city': city,
            'state': state,
            'postal_code': postalCode,
            'country': country,
            'phone': phone,
            'birth_date': dateOfBirth,
            'password': password,
        }

        user = client.users.create(data)

        return render(request,'createUser.html')

    #countryCodes = codes.getCountryCodes
    
    #return render(request, 'createUser.html', {"countryCodes": countryCodes})
    return render(request, 'createUser.html')


def listUsers(request):
    users = client.users.stream()

    context = {
        'isSuccess' : True,
        'users' : users
    }

    return render(request,'listUsers.html', context)

def listCards(request):
    token  = 'b7271c0b-f5b5-40b2-968b-f924cf5f8b33'

    cards = client.cards.list_for_user(token)

    context = {
        'isSuccess' : True,
        'cards' : cards
    }

    return render(request,'listCards.html', context)


def listCardProducts(request):
    cardProducts = client.card_products.list()

    context = {
        'isSuccess' : True,
        'cardProducts' : cardProducts
    }

    return render(request,'listCardProducts.html', context)


    





def createCardProduct(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        startDate = request.POST.get("startDate")

        data = {
            'name': name,
            'start_date': startDate
        }

        cardProduct = client.card_products.create(data)

        return render(request,'createCardProduct.html')

    return render(request, 'createCardProduct.html')


def createCard(request):
    if request.method == 'POST':
        #name = request.POST.get("name")
        #startDate = request.POST.get("startDate")

        name_line_1 = {
            'value': 'Mudasir Yasin'
        }

        text = {
            'name_line_1': name_line_1
        }

        card_personalization = {
            'text': text
        }

        recipient_address = {
            'address1': 'None',
            'city': 'New York',
            'state': 'New York',
            'postal_code': '54000'
        }

        shipping = {
            'recipient_address': recipient_address
        }

        fulfillment = {
            'card_personalization': card_personalization,
            'shipping': shipping
        }

        data = {
            'user_token': 'b7271c0b-f5b5-40b2-968b-f924cf5f8b33',
            'card_product_token': 'fa74b8fd-c854-4b35-a5bd-5989196e11e3',
            'fulfillment': fulfillment
        }

        card = client.cards.create(data)

        return render(request,'createCard.html')

    return render(request, 'createCard.html')



def createUser(request):
    if request.method == 'POST':
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postalCode = request.POST.get("postalCode")
        country = request.POST.get("country")
        phone = request.POST.get("phone")
        dateOfBirth = request.POST.get("dateOfBirth")
        password = request.POST.get("password")
        #parentToken  = request.POST.get("lastName")
        #company = request.POST.get("lastName")
        #identifications = request.POST.get("lastName")

        data = {
            'first_name': firstName,
            'last_name': lastName,
            'gender': gender,
            'email': email,
            'address1': address,
            'city': city,
            'state': state,
            'postal_code': postalCode,
            'country': country,
            'phone': phone,
            'birth_date': dateOfBirth,
            'password': password,
        }

        print(data)
        createdUser = client.users.create(data)

        return render(request,'createUser.html')

    #countryCodes = codes.getCountryCodes
    
    #return render(request, 'createUser.html', {"countryCodes": countryCodes})
    return render(request, 'createUser.html', {'firstName': 'Mudasir'})



def getCards():
    cards = {}
    cards['1'] = '1'
    cards['2'] = '2'
    cards['3'] = '3'

    base_url = "https://sandbox-api.marqeta.com/v3/"
    application_token = "e5f1fdd8-de74-4d38-a66b-e094626d9014"
    access_token = "bdcfe703-b344-4f23-87c0-cc34284b9330"
    timeout = 60 # seconds

    client = Client(base_url, application_token, access_token, timeout)

    token  = 'b7271c0b-f5b5-40b2-968b-f924cf5f8b33'

    cards = client.cards.list_for_user(token)

    return cards
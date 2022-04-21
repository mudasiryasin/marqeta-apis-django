from django.shortcuts import render
import requests
import base64
import json


tokens = 'e5f1fdd8-de74-4d38-a66b-e094626d9014:bdcfe703-b344-4f23-87c0-cc34284b9330'
encoded = base64.b64encode(tokens.encode('ascii'))
headers = {
     'Content-Type': 'application/json',
     'Authorization': 'Basic ' + encoded.decode('utf-8')
}


def dashboard(request):
    return render(request, 'dashboard.html')

def listUsers(request):
    url = "https://sandbox-api.marqeta.com/v3/users"
    response = requests.get(url, headers=headers)
    
    isSuccess = False
    message = ''
    data = ''
    if response.status_code == 200:
        data = json.loads(response.text)['data']
        isSuccess = True
    elif response.status_code == 400:
        message = 'Bad request!'
    else:
        message = 'Server error!'
    
    return render(request,'listUsers.html', {'users': data, 'isSuccess': isSuccess, 'message': message})

def createUser(request):
    if request.method == 'POST':
        url = "https://sandbox-api.marqeta.com/v3/users"

        data = json.dumps({
            "first_name": request.POST.get("firstName"),
            "last_name": request.POST.get("lastName"),
            "gender": request.POST.get("gender"),
            "email": request.POST.get("email"),
            "address": request.POST.get("address"),
            "city": request.POST.get("city"),
            "state": request.POST.get("state"),
            "postal_code": request.POST.get("postalCode"),
            "country": request.POST.get("country"),
            "phone": request.POST.get("phone"),
            "birth_date": request.POST.get("dateOfBirth")
        })

        response = requests.post(url, headers=headers, data=data)

        isSuccess = False
        message = ''

        if response.status_code == 201:
            isSuccess = True
            message = 'User created successfully!'
        elif response.status_code == 400:
            message = 'User input error / Bad request!'
        elif response.status_code == 409:
            message = 'Request already processed with a different payload!'
        elif response.status_code == 412:
            message = 'Pre-condition setup issue!'
        else:
            message = 'Server error!'

        return render(request,'createUser.html', {'isSuccess': isSuccess, 'message': message})

    return render(request, 'createUser.html')

def listCards(request):
    user_id = 'b7271c0b-f5b5-40b2-968b-f924cf5f8b33'
    url = "https://sandbox-api.marqeta.com/v3/cards/user/" + user_id
    
    response = requests.get(url, headers=headers)
    
    isSuccess = False
    message = ''
    data = ''
    if response.status_code == 200:
        data = json.loads(response.text)['data']
        isSuccess = True
    elif response.status_code == 400:
        message = 'User input error / Bad request!'
    else:
        message = 'Server error!'

    return render(request,'listCards.html', {'cards': data, 'isSuccess': isSuccess, 'message': message})

def createCard(request):
    if request.method == 'POST':
        url =   "https://sandbox-api.marqeta.com/v3/cards?show_cvv_number="+ str(request.POST.get("showCVV")) + "&&show_pan="+ str(request.POST.get("showPAN"))

        data = json.dumps({
            "user_token": request.POST.get("userToken"),
            "card_product_token": request.POST.get("cardProductToken"),
            "token": request.POST.get("cardToken"),
            "fulfillment": {
                "card_personalization": {
                    "text": {
                        "name_line_1": {
                            "value": request.POST.get("name")
                        }
                    }
                },
                "shipping": {
                    "recipient_address": {
                        "address1": request.POST.get("address"),
                        "city": request.POST.get("city"),
                        "state": request.POST.get("state"),
                        "postal_code": request.POST.get("postalCode")
                    }
                }
            }
        })

        response = requests.post(url, headers=headers, data=data)

        isSuccess = False
        message = ''
        if response.status_code == 201:
            isSuccess = True
            message = 'Card created successfully!'
        elif response.status_code == 400:
            message = 'User input error / Bad request!'
        elif response.status_code == 409:
            message = 'Token already associated with a different payload!'
        else:
            message = 'Server error!'

        return render(request,'createCard.html', {'isSuccess': isSuccess, 'message': message})

    return render(request, 'createCard.html')

def listCardProducts(request):
    url = "https://sandbox-api.marqeta.com/v3/cardproducts"
    
    response = requests.get(url, headers=headers)
    
    isSuccess = False
    message = ''
    data = ''
    if response.status_code == 200:
        data = json.loads(response.text)['data']
        isSuccess = True
    elif response.status_code == 400:
        message = 'Bad request!'
    else:
        message = 'Server error!'
    
    return render(request,'listCardProducts.html', {'cardProducts': data, 'isSuccess': isSuccess, 'message': message})

def createCardProduct(request):
    if request.method == 'POST':
        url = "https://sandbox-api.marqeta.com/v3/cardproducts"

        data = json.dumps({
            "name": request.POST.get("name"),
            "start_date": request.POST.get("startDate")
        })

        response = requests.post(url, headers=headers, data=data)

        isSuccess = False
        message = ''
        if response.status_code == 201:
            isSuccess = True
            message = 'Card product created successfully!'
        elif response.status_code == 400:
            message = 'Bad request!'
        elif response.status_code == 409:
            message = 'Token already associated with a different payload!'
        else:
            message = 'Server error!'

        return render(request,'createCardProduct.html', {'isSuccess': isSuccess, 'message': message})

    return render(request, 'createCardProduct.html')

def getUserTokens():
    url = "https://sandbox-api.marqeta.com/v3/users"
    
    response = requests.get(url, headers=headers)
    
    userTokens = {}
    if response.status_code == 200:
        users = json.loads(response.text)['data']
        for user in users:
            userTokens[user['first_name'] + ' ' + user['last_name']] = user['token']
    return userTokens

def getCardProductTokens():
    url = "https://sandbox-api.marqeta.com/v3/cardproducts"
    
    response = requests.get(url, headers=headers)
    
    cardProductTokens = {}
    if response.status_code == 200:
        cardProducts = json.loads(response.text)['data']
        for cardProduct in cardProducts:
            cardProductTokens[cardProduct['name']] = cardProduct['token']
    return cardProductTokens
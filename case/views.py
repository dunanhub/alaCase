import os
from pyexpat.errors import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from alaCase import settings
from .models import *
import qrcode
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import json


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    else:
        return render(request, 'login.html')


def registration_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if User.objects.filter(username=username).first():
            messages.error(request, "This username is already taken")
            check = "taken"
            context = {
                'check': check
            }
            return render(request, 'registration.html', context)

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()

        check = ""
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            check = "taken"
            context = {
                'check': check
            }
            return render(request, 'index.html', context)

        messages.success(request, "Your account has been signed up successfully!")
        return redirect('login')

    return render(request, "registration.html")


def logout_view(request):
    logout(request)
    return redirect('login')


def generate_qr_code(request):
    favorites = json.loads(request.COOKIES.get('favorites', '[]'))
    product_details = ', '.join([item['name'] for item in favorites])
    message = f"Я хочу заказать следующие продукты: {product_details}"
    url = f"https://api.whatsapp.com/send?phone=+77711527761&text={message}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img_qr = qr.make_image(fill='black', back_color='white').convert('RGB')

    icon_path = 'case/static/icon.png'
    icon = Image.open(icon_path)

    width, height = img_qr.size
    icon_size = width // 4
    icon = icon.resize((icon_size, icon_size))

    pos = ((width - icon_size) // 2, (height - icon_size) // 2)
    img_qr.paste(icon, pos, mask=icon)

    response = HttpResponse(content_type="image/png")
    img_qr.save(response, "PNG")
    return response


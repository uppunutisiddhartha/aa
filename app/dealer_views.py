from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import *



# Dealer Registration
def dealer_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        state = request.POST.get('state')
        city = request.POST.get('city')
        name_of_company = request.POST.get('name_of_company')

        if password != confirm_password:
            return render(request, 'auths/dealer_register.html', {'error': "Passwords do not match"})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'auths/dealer_register.html', {'error': "Username already exists"})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'auths/dealer_register.html', {'error': "Email already exists"})

        user = CustomUser.objects.create(
            username=username,
            password=make_password(password),
            email=email,
            phone=phone,
            name=name,
            state=state,
            city=city,
            role='dealer',
        )

        Dealer.objects.create(user=user, name_of_company=name_of_company)

        login(request, user)
        return redirect('login')  

    return render(request, 'auths/dealer_register.html')


# Dealer Dashboard
def dealer_dashboard(request):
    return render(request, 'dealer_dashboard.html')
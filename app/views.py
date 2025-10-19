from django.shortcuts import render

# Create your views here.


def index(request):
    
    return render(request,"index.html")


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Customer, Dealer


# Customer Registration
def customer_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')

        if password != confirm_password:
            return render(request, 'auths/customer_register.html', {'error': "Passwords do not match"})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'auths/customer_register.html', {'error': "Username already exists"})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'auths/customer_register.html', {'error': "Email already exists"})

        user = CustomUser.objects.create(
            username=username,
            password=make_password(password),
            email=email,
            phone=phone,
            name=name,
            state=state,
            city=city,
            role='customer',
        )

        Customer.objects.create(user=user, address=address)

        login(request, user)
        return redirect('login')  

    return render(request, 'auths/customer_register.html')




# Login view for both (same login page, redirect based on role)
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'dealer':
                return redirect('dealer_dashboard')
            else:
                return redirect('index')
        else:
            return render(request, 'auths/login.html', {'error': 'Invalid username or password'})

    return render(request, 'auths/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

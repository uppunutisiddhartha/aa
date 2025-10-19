from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .models import Dealer, Flight
from datetime import datetime



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
        return redirect('rolelogin')  

    return render(request, 'auths/dealer_register.html')


# Dealer Dashboard
@login_required
def dealer_dashboard(request):
    dealer = Dealer.objects.get(user=request.user)
    hotels = dealer.hotels.all()
    flights = dealer.flights.all()
    return render(request, 'dealer_dashboard.html', {
        'hotels': hotels,
        'flights': flights,
    })

@login_required
def add_hotel(request):
    if request.method == 'POST':
        dealer = Dealer.objects.get(user=request.user)
        name = request.POST.get('name')
        location = request.POST.get('location')
        description = request.POST.get('description')

        if name and location:
            Hotel.objects.create(
                dealer=dealer,
                name=name,
                location=location,
                description=description
            )
            return redirect('dealer_dashboard')
        else:
            return render(request, 'dashboard/add_hotel.html', {'error': 'All fields are required.'})

    return render(request, 'add_hotel.html')


@login_required
def add_flight(request):
    if request.method == 'POST':
        dealer = Dealer.objects.get(user=request.user)

        airline = request.POST.get('airline')
        flight_number = request.POST.get('flight_number')
        from_city = request.POST.get('from_city')
        to_city = request.POST.get('to_city')
        departure_time_str = request.POST.get('departure_time')  # e.g. '2025-12-15T04:57'
        arrival_time_str = request.POST.get('arrival_time')

        # Convert datetime-local string (with 'T') to Python datetime object
        try:
            departure_time = datetime.fromisoformat(departure_time_str)
            arrival_time = datetime.fromisoformat(arrival_time_str)
        except ValueError:
            return render(request, 'add_flight.html', {'error': 'Invalid date/time format'})

        total_seats = request.POST.get('total_seats')
        available_seats = request.POST.get('available_seats')
        price = request.POST.get('price')

        if all([airline, flight_number, from_city, to_city, departure_time, arrival_time, total_seats, available_seats, price]):
            Flight.objects.create(
                dealer=dealer,
                airline=airline,
                flight_number=flight_number,
                from_city=from_city,
                to_city=to_city,
                departure_time=departure_time,
                arrival_time=arrival_time,
                total_seats=int(total_seats),
                available_seats=int(available_seats),
                price=price
            )
            return redirect('dealer_dashboard')
        else:
            return render(request, 'add_flight.html', {'error': 'Please fill in all fields.'})

    return render(request, 'add_flight.html')


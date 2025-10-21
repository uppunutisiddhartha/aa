from django.shortcuts import render,redirect
from .models import *
from datetime import datetime, date, time, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.


def index(request):
   
    return render(request,"index.html")


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
        return redirect('rolelogin')  

    return render(request, 'auths/customer_register.html')




# Login view for both (same login page, redirect based on role)
def rolelogin(request):
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

# Logout view
def logout_view(request):
    logout(request)
    return redirect('rolelogin')

# Flights Booking Views
@login_required(login_url='rolelogin')
def flight_booking(request):

    flight=Flight.objects.all()
    return render(request, 'flights_booking.html' ,{'flight':flight})


# Hotel Booking Views
@login_required(login_url='rolelogin')
def hotel_booking(request):
    hotels=Hotel.objects.all()
    return render(request,'hotel_booking.html',{'hotels':hotels}) 
from django.utils import timezone

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.all()

    # Optional: get check-in and check-out from query params
    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')

    today = timezone.now().date()

    check_in = timezone.datetime.strptime(check_in_str, '%Y-%m-%d').date() if check_in_str else today
    check_out = timezone.datetime.strptime(check_out_str, '%Y-%m-%d').date() if check_out_str else today

    bookings = Booking.objects.filter(hotel_room__hotel=hotel)

    for room in rooms:
        room.bookings = []
        for booking in bookings:
            if booking.hotel_room.id == room.id:
                # Only consider booking if it overlaps with selected dates
                if booking.check_out >= check_in and booking.check_in <= check_out:
                    room.bookings.append({
                        'user': booking.user,
                        'check_in': booking.check_in,
                        'check_out': booking.check_out,
                        'num_persons': getattr(booking, 'num_persons', None),
                    })

    context = {
        'hotel': hotel,
        'rooms': rooms,
        'check_in': check_in,
        'check_out': check_out,
    }
    return render(request, 'hotel_detail.html', context)


from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import HotelRoom, Booking

@login_required
def book_room(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id)

    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        num_persons = int(request.POST.get("num_persons"))
        address_proof = request.FILES.get("address_proof")

        # Convert dates
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect("book_room", room_id=room.id)

        # Validate dates
        if check_in_date >= check_out_date:
            messages.error(request, "Check-out must be after check-in.")
            return redirect("book_room", room_id=room.id)

        if num_persons > room.capacity:
            messages.error(request, f"Number of persons exceeds room capacity ({room.capacity}).")
            return redirect("book_room", room_id=room.id)

        # Check overlapping bookings
        overlapping = Booking.objects.filter(
            hotel_room=room,
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        )
        if overlapping.exists():
            messages.error(request, "Room is already booked for the selected dates.")
            return redirect("book_room", room_id=room.id)

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            hotel_room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            num_persons=num_persons,
            address_proof=address_proof
        )

        # ✅ Send confirmation email
        subject = f"Booking Confirmation for {room.hotel.name} - Room {room.room_number}"
        message = (
            f"Dear {request.user.name},\n\n"
            f"Your booking for Room {room.room_number} at {room.hotel.name} has been confirmed.\n"
            f"Check-in: {check_in_date}\n"
            f"Check-out: {check_out_date}\n"
            f"Number of Guests: {num_persons}\n\n"
            f"Thank you for booking with us!"
        )
        recipient_list = [request.user.email]

        try:
            send_mail(subject, message, None, recipient_list, fail_silently=False)
        except Exception as e:
            messages.warning(request, f"Booking confirmed but email failed to send: {e}")

        messages.success(request, f"Room {room.room_number} booked successfully! A confirmation email has been sent.")
        return redirect("my_bookings")

    return render(request, "book_room.html", {"room": room})



@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('hotel_room__hotel')
    return render(request, "my_bookings.html", {"bookings": bookings})

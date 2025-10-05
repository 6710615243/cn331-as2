from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import RoomData, Reservation
from .forms import ReservationForm, RegistorForm, UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You have logged in successfully.", extra_tags="login")
            return redirect('index') 
        else:
            messages.error(request, "Invalid username or password.",  extra_tags="login")
            return render(request, 'rooms/login.html')
    
    return render(request, 'rooms/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')

def index(request):
    rooms = RoomData.objects.all()
    context =  {'rooms' : rooms}
    return render(request, 'rooms/index.html', context)

def register(request):
    if request.method == "POST":
        form  = RegistorForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("index")
        else:
            form  = RegistorForm()
        return render(request, "rooms/register.html", {"form" : form})

def reserve_room(request, room_id):
    room = get_object_or_404(RoomData, id=room_id)
    
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to reserve a room.")
        return redirect("login_user")

    # Handle a POST request (form submission)
    if request.method == "POST":
        # Check if the user already has a reservation
        # This check is crucial to prevent multiple reservations if that is your business rule
        if Reservation.objects.filter(user=request.user).exists():
            messages.error(request, "You already have a room reservation.")
            return redirect("index")

        # Check room availability
        if not room.room_available or room.room_hour <= 0:
            messages.error(request, "This room is not available.")
            return redirect("index")
            
        # Create the reservation
        Reservation.objects.create(user=request.user, room=room)
        
        # Update room availability
        room.room_hour -= 1
        if room.room_hour == 0:
            room.room_available = False
        room.save()

        messages.success(request, f"You have successfully reserved {room.room_name}.")
        return redirect("index")
        
    # Handle a GET request (initial page load)
    else:
        context = {'room': room}
        return render(request, 'rooms/reserve.html', context)

@login_required(login_url='login_user')
def cancel_reservation(request):
    reservation = Reservation.objects.filter(user=request.user).first()
    if reservation:
        room = reservation.room
        room.room_hour += 1
        room.room_available = True
        room.save()
        reservation.delete()
        messages.success(request, "Reservation cancelled successfully.")
    else:
        messages.error(request, "You have no reservation to cancel.")
    return redirect("index")

def login_admin(request):
    return redirect('admin')
    

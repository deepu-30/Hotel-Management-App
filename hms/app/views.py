from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile, Availability, Booking
from django.http import HttpResponse
import requests

# Register
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, role=role)

        #calling serverless email
        requests.post("http://localhost:3000/send", json={
            "type": "SIGNUP_WELCOME",
            "to": "test@tempmail.com"
        })


        return redirect('/')
    return render(request, 'register.html')

# Login
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/dashboard/')
    return render(request, 'login.html')

# Dashboard
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role == 'doctor':
        slots = Availability.objects.filter(doctor=request.user)
        return render(request, 'doctor.html', {'slots': slots})

    else:
        slots = Availability.objects.filter(is_booked=False)
        return render(request, 'patient.html', {'slots': slots})

# Add slot (Doctor)
from datetime import datetime
from django.http import HttpResponse

def add_slot(request):
    if request.method == "POST":
        date_input = request.POST['date']
        time_input = request.POST['time']

        # Convert to datetime
        slot_datetime = datetime.strptime(f"{date_input} {time_input}", "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()

        # ❌ Block past slots
        if slot_datetime < current_datetime:
            return HttpResponse("❌ Cannot select past date/time")

        Availability.objects.create(
            doctor=request.user,
            date=date_input,
            time=time_input
        )
        

        return redirect('/dashboard/')

    return render(request, 'add_slot.html')

# Book slot (Patient)
def book_slot(request, slot_id):
    slot = Availability.objects.get(id=slot_id)

    if slot.is_booked:
        return HttpResponse("Already booked")

    Booking.objects.create(
        patient=request.user,
        slot=slot
    )

    slot.is_booked = True
    slot.save()

    # after slot.save()

    create_calendar_event(
        doctor=slot.doctor.username,
        patient=request.user.username,
        slot=slot
    )

    requests.post("http://localhost:3000/send", json={
        "type": "BOOKING_CONFIRMATION",
        "to": "test@tempmail.com"
    })

    return redirect('/dashboard/')

import pickle
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def create_calendar_event(doctor, patient, slot):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

    service = build('calendar', 'v3', credentials=creds)

    start_datetime = datetime.combine(slot.date, slot.time)
    end_datetime = start_datetime + timedelta(minutes=30)

    event = {
        'summary': f'Appointment with {patient}',
        'description': 'Hospital Appointment',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    event = service.events().insert(
        calendarId='primary',
        body=event
    ).execute()

    print("📅 Event created:", event.get('htmlLink'))

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/')


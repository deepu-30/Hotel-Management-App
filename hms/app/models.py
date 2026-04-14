from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

# Role model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)  # doctor / patient

# Doctor availability
class Availability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

# Booking model
class Booking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Availability, on_delete=models.CASCADE)
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here
class Doctor(models.Model):
    department = (
        ('Allergy & Clinical Immunology' , 'Allergy & Clinical Immunology'),
        ('Anesthesiologists' , 'Anesthesiologists'),
        ('Blood Screening', 'Blood Screening'),
        ('Cardiology', "Cardiology"),
        ('Dentistry', "Dentistry"),
        ('ENT Specialists', "ENT Specialists"),
        ('Eye Care', 'Eye Care'),
        ('Gastroenterologists' , 'Gastroenterologists'),       
        ('Neuroanatomy', 'Neuroanatomy'),
        ('Oncologists' , 'Oncologists'),
        ('Pediatricians' , 'Pediatricians'),
        ('Physical Therapy', 'Physical Therapy'),
    )
    name = models.CharField(max_length=256)
    email = models.EmailField(null=True)
    qualification = models.CharField(max_length=256)
    specialization = models.CharField(choices=department, max_length=100)
    hospitalName = models.CharField(max_length=150)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Doctor'
    
    def __str__(self):
        return self.name

class Timeslots(models.Model):
    doctor = models.ForeignKey('Doctor' , on_delete=models.CASCADE)
    datetimeslot = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Timeslots'

class Appointment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    meetingId = models.CharField(max_length=250)
    doctor = models.ForeignKey('Doctor' , on_delete=models.CASCADE , null=True)
    slot = models.ForeignKey('Timeslots' , on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Appointment'

    def __str__(self):
        return self.meetingId



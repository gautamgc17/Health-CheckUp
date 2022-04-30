from django.contrib import admin
from appointment import models

# Register your models here
admin.site.register([
    models.Doctor,
    models.Timeslots,
    models.Appointment,
])

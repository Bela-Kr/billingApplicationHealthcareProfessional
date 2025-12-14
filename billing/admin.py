from django.contrib import admin
from .models import Patient, Service

admin.site.register(Patient)
admin.site.register(Service)
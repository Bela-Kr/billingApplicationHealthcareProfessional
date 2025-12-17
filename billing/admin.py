from django.contrib import admin
from .models import Patient, Service, Bill

admin.site.register(Patient)
admin.site.register(Bill)
admin.site.register(Service)
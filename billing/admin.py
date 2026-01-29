"""
Configuration for the Django administrative interface.
Registers models to make them manageable via the admin panel.
"""

from django.contrib import admin
from .models import Bill, Patient, Service

admin.site.register(Patient)
admin.site.register(Bill)
admin.site.register(Service)
"""
URL configuration for the billing application.
Maps URL patterns to view functions.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("patients/", views.patient_list, name="patient_list"),
    path("patients/create/", views.create_patient, name="create_patient"),
    path("patients/<int:pk>/", views.patient_detail, name="patient_detail"),
    path("patients/<int:patient_id>/records/create/", views.create_medical_record, name="create_medical_record"),
    
    path("bills/", views.bill_list, name="bill_list"),
    path("bills/create/", views.create_bill, name="create_bill"),
    
    path("services/", views.service_list, name="service_list"),
    path("services/create/", views.create_service, name="create_service"),
]
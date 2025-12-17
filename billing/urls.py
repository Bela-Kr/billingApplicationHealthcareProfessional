from django.urls import path
from . import views

urlpatterns = [
    path("patients/", views.patientList, name="patientList"),
    path("patients/add", views.createPatient, name="createPatient"),
    path("bills/", views.billList, name="billList"),
    path("bills/add", views.createBill, name="createBill"),
]
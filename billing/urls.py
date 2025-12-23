from django.urls import path
from . import views

urlpatterns = [
    path("patients/", views.patientList, name="patientList"),
    path("patients/add", views.createPatient, name="createPatient"),
    path("bills/", views.billList, name="billList"),
    path("bills/add", views.createBill, name="createBill"),
    path("patients/<int:patient_id>/neuer-eintrag",views.createMedicalRecord, name="createMedicalRecord"),
    path("patients/<int:pk>", views.patientDetails, name="patientDetails"),
    path("services/", views.serviceList, name="serviceList"),
    path("services/new", views.createService, name="createService"),
]
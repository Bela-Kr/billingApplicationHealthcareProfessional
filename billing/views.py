from decimal import Decimal
from typing import Any, Dict

from django.db.models import Sum, F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Patient, Bill, MedicalRecord, Service
from .forms import (
    BillForm, 
    PatientForm, 
    MedicalRecordForm, 
    ServiceForm, 
)

def patient_list(request: HttpRequest) -> HttpResponse:
    """
    Displays a list of all patients.
    """
    all_patients = Patient.objects.all()
    
    context = {
        'patients': all_patients
    }
    
    return render(request, 'billing/patient_list.html', context)

def create_patient(request: HttpRequest) -> HttpResponse:
    """
    Handles the creation of a new patient record.
    """
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("patient_list")
    else:
        form = PatientForm()

    return render(request, 'billing/patient_form.html', {'form': form})

def bill_list(request: HttpRequest) -> HttpResponse:
    """
    Displays a filtered list of bills and calculates the total open amount.
    """
    bills = Bill.objects.all().order_by("-issue_date")

    patient_id = request.GET.get("patient")
    if patient_id:
        bills = bills.filter(patient_id=patient_id)

    month_input = request.GET.get("month")
    if month_input:
        bills = bills.filter(issue_date__month=month_input)

    # Calculate total revenue from the filtered bills using database aggregation
    total_data = bills.aggregate(
        total_sum=Sum(F('items__price') * F('items__quantity'))
    )

    open_amount = total_data["total_sum"] or Decimal(0)
    all_patients = Patient.objects.all()

    context = {
        "bills": bills,
        "open_amount": open_amount,
        "patients": all_patients,
    }

    return render(request, "billing/bill_list.html", context)

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from decimal import Decimal
from .models import Patient, Bill, MedicalRecord, Service, InvoiceItem
from .forms import BillForm, PatientForm, MedicalRecordForm, ServiceForm


def create_bill(request: HttpRequest):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save()

            services_selected = form.cleaned_data['selected_services']

            for service in services_selected:
                InvoiceItem.objects.create(
                    bill=bill,
                    service=service,
                    price=service.price, 
                    quantity=1,
                )
            
            return redirect('bill_list')
    else:
        form = BillForm()

    return render(request, 'billing/bill_form.html', {'form': form})

def create_medical_record(request: HttpRequest, patient_id: int) -> HttpResponse:
    """
    Adds a medical note/diagnosis to a specific patient.
    """
    patient = get_object_or_404(Patient, pk=patient_id)

    if request.method == "POST":
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            return redirect("patient_detail", pk=patient.id)
    else:
        form = MedicalRecordForm()
        
    context = {
        "form": form,
        "patient": patient
    }
    return render(request, "billing/record_form.html", context)

def patient_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Shows detailed information for a specific patient.
    """
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, "billing/patient_detail.html", {"patient": patient})

def service_list(request: HttpRequest) -> HttpResponse:
    """
    Displays the catalog of available services/products.
    """
    services = Service.objects.all()
    return render(request, "billing/service_list.html", {"services": services})

def create_service(request: HttpRequest) -> HttpResponse:
    """
    Adds a new item to the service catalog.
    """
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("service_list")  
    else:
        form = ServiceForm()
    
    return render(request, "billing/service_form.html", {"form": form})
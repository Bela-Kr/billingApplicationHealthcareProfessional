from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from .models import Patient, Bill, MedicalRecord, Service
from .forms import BillForm, PatientForm, MedicalRecordForm, ServiceForm

def patientList(request):
    all_patients = Patient.objects.all()
    
    context = {
        'patients': all_patients
    }
    
    return render(request, 'billing/patientList.html', context)

def createPatient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("patientList")
    else:
        form = PatientForm()

    return render(request, 'billing/patientForm.html', {'form': form})

def billList(request):
    bills = Bill.objects.all().order_by("-zahlungsDatum")

    total_open_data = bills.filter(status="SENT").aggregate(
        total_sum = Sum("services__preis")
    )

    open_amount = total_open_data["total_sum"] or 0

    context = {
        "Bill":bills,
        "open_amount": open_amount,
    }

    return render(request, "billing/billList.html", context)

def createBill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('billList')
    else:
        form = BillForm()

    return render(request, 'billing/billForm.html', {'form': form})

def createMedicalRecord(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    if request.method == "POST":
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()

            return redirect("patientDetails", pk = patient.id)
    else:
        form = MedicalRecordForm()
        
    return render(request, "billing/createRecord.html", {"form":form, "patient":patient})

def patientDetails(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    return render(request, "billing/patientDetail.html", {"patient":patient})

def serviceList(request):
    services = Service.objects.all()

    context = {"services":services}

    return render(request, "billing/serviceList.html", context)

def createService(request):

    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            
            return redirect("serviceList")  
    else:
        form = ServiceForm()
    
    return render(request, "billing/createService.html", {"form": form})
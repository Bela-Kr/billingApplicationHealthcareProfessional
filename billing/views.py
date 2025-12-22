from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Bill, MedicalRecord
from .forms import BillForm, PatientForm, MedicalRecordForm

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

    context = {"Bill":bills}

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
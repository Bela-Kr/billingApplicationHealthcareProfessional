from django.shortcuts import render, redirect
from .models import Patient, Bill
from .forms import BillForm, PatientForm

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
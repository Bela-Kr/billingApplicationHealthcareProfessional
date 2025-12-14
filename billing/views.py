from django.shortcuts import render, redirect
from .models import Patient
from .forms import PatientForm

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
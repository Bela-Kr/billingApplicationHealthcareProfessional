from django import forms
from django.forms import inlineformset_factory

from .models import Patient, Bill, Service, MedicalRecord, InvoiceItem

class PatientForm(forms.ModelForm):
    """
    Form for creating and updating Patient records.
    """
    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "address", "email"]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Max'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Mustermann'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Musterstraße 1'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'max@example.com'
            }),
        }


class ServiceForm(forms.ModelForm):
    """
    Form for managing Services (Products/Treatments).
    """
    class Meta:
        model = Service
        fields = ["name", "price", "description", "billing_code"]

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "price": forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            "billing_code": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class MedicalRecordForm(forms.ModelForm):
    """
    Form for adding medical notes to a patient.
    """
    class Meta:
        model = MedicalRecord
        fields = ["diagnosis", "treatment", "notes"]

        widgets = {
            "diagnosis": forms.TextInput(attrs={'class': 'form-control'}),
            "treatment": forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            "notes": forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class BillForm(forms.ModelForm):
    # We explicitly define this field to get the Checkbox UI back
    selected_services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Services"
    )

    class Meta:
        model = Bill
        # We exclude 'services' here because we handle saving them manually in the view
        fields = ["patient", "issue_date", "due_date", "status"]
        
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
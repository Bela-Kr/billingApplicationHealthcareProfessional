from django import forms
from .models import Patient, Bill, Service

class PatientForm(forms.ModelForm):
    class Meta():
        model = Patient
        fields = ["firstName", "lastName", "address", "email"]

widgets = {
    'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Max'}),
    'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mustermann'}),
    'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Musterstraße 1'}),
    'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'max@example.com'}),
}

class BillForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Leistungen"
    )
    class Meta():
        model = Bill
        fields = ["patient", "zahlungsDatum", "status", "services"]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select form-select-lg shadow-sm'}),
            'status': forms.Select(attrs={'class': 'form-select form-select-lg shadow-sm'}),
        }
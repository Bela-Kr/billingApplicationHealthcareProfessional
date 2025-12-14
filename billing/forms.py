from django import forms
from .models import Patient

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
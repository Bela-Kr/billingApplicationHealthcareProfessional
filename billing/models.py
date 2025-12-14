from django.db import models

class Patient(models.Model):
    # Patienteninformationen
    lastName = models.CharField(max_length=50, verbose_name="Nachname")
    firstName = models.CharField(max_length=50, verbose_name="Vorname")
    address = models.TextField(verbose_name="Adresse")
    email = models.EmailField(blank=True, verbose_name="Email Adresse")

    # Darstellung von Vor und Nachname im Admin panel
    def __str__ (self):
        return f"{self.firstName} {self.lastName}"

class Service(models.Model):
    serviceName = models.CharField(max_length=100, verbose_name="Leistung")
    price = models.IntegerField(default=0, verbose_name="Preis (€)")
    description = models.TextField(blank=True, verbose_name="Beschreibung")

    def __str__ (self):
        return f"{self.serviceName} ({self.price} €)"
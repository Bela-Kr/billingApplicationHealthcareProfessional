import uuid
from django.utils import timezone
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
    preis = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name="Preis (€)")
    beschreibung = models.TextField(blank=True, verbose_name="Beschreibung")

    def __str__ (self):
        return f"{self.serviceName} ({self.preis} €)"
    
def generateInvoiceNumber():
    today = timezone.now().strftime("%Y%m%d")
    short_uuid = str(uuid.uuid4())[:4].upper()
    return f"{today}-{short_uuid}"

class Bill(models.Model):
    patient = models.ForeignKey(Patient, verbose_name=("Rechnungs-Patient"), on_delete=models.CASCADE)
    rechnungsNummer = models.CharField(max_length=20, default=generateInvoiceNumber, unique=True, editable=False)
    zahlungsDatum = models.DateField()

    STATUS_CHOICES = [("DRAFT", "Entwurf"), ("SENT", "Gesendet"), ("PAID", "Bezahlt")]
    status = models.CharField(choices=STATUS_CHOICES,default="DRAFT",  max_length=20)

    services = models.ManyToManyField(Service)

    class meta():
        ordering = ["-date"]

    def __str__(self):
        return f"Rechnung {self.rechnungsNummer} ({self.patient})"
    
    def getTotal(self):
        total = sum(Service.preis for Service in self.services.all())
        return total

    
class InvoiceItem(models.Model):
    rechnung = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="Items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="Leistung")
    preis = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preis")

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.service.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service.serviceName} auf {self.invoice.invoice_number}"
    ## Hier nochmal Erklärungen s
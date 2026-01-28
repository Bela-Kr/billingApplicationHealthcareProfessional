import uuid
from decimal import Decimal
from typing import List

from django.db import models
from django.utils import timezone


class Patient(models.Model):
    """
    Represents a patient/client in the system.
    """
    last_name = models.CharField(
        max_length=50,
        verbose_name="Last Name"
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name="First Name"
    )
    address = models.TextField(
        verbose_name="Address"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email Address"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Service(models.Model):
    """
    Represents a standard medical service or product offered.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Service Name"
    )
    price = models.DecimalField(
        default=0,
        max_digits=6,
        decimal_places=2,
        verbose_name="Price (€)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    # CharField because billing codes can have leading zeros (e.g., '01')
    # or letters which DecimalField cannot handle.
    billing_code = models.CharField(
        max_length=10,
        verbose_name="Billing Code"
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.price} €)"


def generate_invoice_number() -> str:
    """
    Generates a unique invoice number format: YYYYMMDD-UUID.

    Returns:
        str: A unique string identifier.
    """
    today = timezone.now().strftime("%Y%m%d")
    short_uuid = str(uuid.uuid4())[:4].upper()
    return f"{today}-{short_uuid}"


class Bill(models.Model):
    """
    Represents an invoice issued to a patient.
    """
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SENT", "Sent"),
        ("PAID", "Paid")
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        verbose_name="Patient",
        related_name="bills"
    )
    invoice_number = models.CharField(
        max_length=20,
        default=generate_invoice_number,
        unique=True,
        editable=False,
        verbose_name="Invoice Number"
    )
    issue_date = models.DateField(
        default=timezone.now,
        verbose_name="Issue Date"
    )
    due_date = models.DateField(
        default=timezone.now,
        verbose_name="Due Date"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT",
        verbose_name="Status"
    )
    services = models.ManyToManyField(
        Service,
        through='InvoiceItem',
        related_name='bills',
        verbose_name="Services"
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"Invoice {self.invoice_number} ({self.patient})"

    def get_total(self) -> Decimal:
        """
        Calculates the total amount of the bill based on associated items.

        Returns:
            Decimal: The sum of all item prices.
        """
        total = sum(item.price for item in self.items.all())
        return Decimal(total)


class InvoiceItem(models.Model):
    """
    Intermediate model linking a Bill and a Service.
    Stores the price at the moment of creation (Snapshot).
    """
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name="items"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="invoice_items"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantity"
    )

    def save(self, *args, **kwargs) -> None:
        """
        Overridden save method to auto-fill price from service if not set.
        """
        if not self.price:
            self.price = self.service.price
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.service.name} on {self.bill.invoice_number}"


class MedicalRecord(models.Model):
    """
    Stores medical notes and history for a patient.
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_records",
        verbose_name="Patient"
    )
    diagnosis = models.CharField(
        max_length=200,
        verbose_name="Diagnosis"
    )
    treatment = models.TextField(
        blank=True,
        verbose_name="Treatment"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    def __str__(self) -> str:
        return f"Record for {self.patient} - {self.created_at.date()}"
"""
Main URL configuration for the project.

This file acts as the central entry point for routing. It:
1. Routes admin requests to the Django Admin interface.
2. Includes the URL patterns from the 'billing' application.
3. Redirects the root URL ('/') to the patient list.
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # Admin Interface
    path("admin/", admin.site.urls),

    # Include urls from the billing app
    # All URLs in billing/urls.py will be prefixed with 'billing/' (e.g., /billing/patients/)
    path("", include("billing.urls")),

    # Root Redirect
    # When a user visits the homepage ('/'), redirect them to the patient list.
    # Note: 'patient_list' must match the name='patient_list' defined in billing/urls.py
    path("", RedirectView.as_view(pattern_name="patient_list"), name="root"),
]
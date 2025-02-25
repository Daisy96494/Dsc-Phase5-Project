from django.urls import path
from . import views

app_name = "jobs"  # ✅ This ensures namespacing is correct

urlpatterns = [
    path("", views.home, name="home"),
    path("results/", views.results, name="results"),  # ✅ Ensure this exists
]

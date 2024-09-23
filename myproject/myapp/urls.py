from django.urls import path
from . import views

urlpatterns = [
    # Define your URL patterns here
    path('', views.run_all_scripts_view, name='run_all_scripts'),
    # Add other paths if needed
]

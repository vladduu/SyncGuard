from django.urls import path
from . import views

urlpatterns = [
    # This maps the root of this app to the dashboard_home view
    path('', views.dashboard_home, name='dashboard_home'),
    path('download/<int:log_id>/', views.download_file, name='download_file'),
]
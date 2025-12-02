from django.urls import path
from django.urls import path, include
from . import views
from .metrics import metrics_view

urlpatterns = [
    path('', views.check_hostname, name='hostname'),
    path('', include('django_prometheus.urls')),
    path('health/', views.healthcheck, name='health'),
    path('prize/', views.change_db, name='db_test'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_hostname, name='hostname'),
    path('health/', views.healthcheck, name='health'),
    path('prize/', views.change_db, name='db_test')
]
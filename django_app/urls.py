from django.urls import path
from . import views

urlpatterns = [
    path('', views.hostname_view, name='hostname'),
    path('health/', views.health_view, name='health'),
    path('db/', views.db_test_view, name='db_test')
]
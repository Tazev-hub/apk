from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students_view, name='students'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('sveden/', views.sveden_view, name='sveden'),
    path('abiturient/', views.abiturient_view, name='abiturient'),
    
]
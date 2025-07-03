from django.urls import path
from .views import export_pdf, export_excel

urlpatterns = [
    path('export/pdf/<int:pk>/', export_pdf, name='export_pdf'),
    path('export/excel/<int:pk>/', export_excel, name='export_excel'),
]

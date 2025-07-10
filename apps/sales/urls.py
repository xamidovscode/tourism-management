from django.urls import path
from .views import export_pdf1, export_excel, export_pdf2

urlpatterns = [
    path('export/pdf1/<int:pk>/', export_pdf1, name='export_pdf1'),
    path('export/pdf2/<int:pk>/', export_pdf2, name='export_pdf2'),
    path('export/excel/<int:pk>/', export_excel, name='export_excel'),

]

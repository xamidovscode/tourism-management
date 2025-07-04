from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from apps.sales.views import export_pdf, export_excel, sale_list

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),

    path('admin/', admin.site.urls),
    # path('admin/', admin_site.urls),

    path('test/export-pdf/<int:pk>/', export_pdf, name='export_pdf'),
    path('test/export-excel/<int:pk>/', export_excel, name='export_excel'),
    path('sales/', sale_list, name='sale_list'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# core/admin.py
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name="custom-dashboard"),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        context = dict(
            self.each_context(request),
            title="Dashboard",
        )
        return TemplateResponse(request, "admin/custom_dashboard.html", context)

admin_site = CustomAdminSite(name='custom_admin')

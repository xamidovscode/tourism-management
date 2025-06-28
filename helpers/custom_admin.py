from django.contrib import admin


ALLOWED_AGENT_MODELS = [
    'sales.Customer',
    'sales.Sale',
    'sales.TourProxy',
]

DISALLOWED_ADMIN_MODELS = [
    'sales.Sale',
    'sales.TourProxy',
]


class RestrictedAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_authenticated:
            key = f"{self.model._meta.app_label}.{self.model.__name__}"

            if request.user.status == 'agent':
                return key in ALLOWED_AGENT_MODELS

            else:
                return key not in DISALLOWED_ADMIN_MODELS

        return True


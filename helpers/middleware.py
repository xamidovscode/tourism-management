from django.utils import translation
from django.conf import settings

class LanguageSwitchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.GET.get('language')

        if lang in dict(settings.LANGUAGES):
            request.session['_language'] = lang
            translation.activate(lang)
        else:
            lang = request.session.get('_language')
            if lang:
                translation.activate(lang)

        response = self.get_response(request)
        return response

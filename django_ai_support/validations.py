from django.core.exceptions import ImproperlyConfigured

from rest_framework.settings import APISettings

def settings_validations(settings:APISettings) -> APISettings:
    
    if not settings.LLM_MODEL:
        raise ImproperlyConfigured("LLM_MODEL can not be None")


    return settings

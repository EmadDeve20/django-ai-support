from django.conf import settings

from rest_framework.settings import APISettings
from django.test.signals import setting_changed


USER_SETTINGS = getattr(settings, "AI_SUPPORT_SETTINGS", None)

DEFAULTS = {
    "TOOLS": [],
    "SYSTEM_PROMPT": "You are the supporter of a bookstore website.",
    "RATE_LIMITER": None,
}

api_settings = APISettings(USER_SETTINGS, DEFAULTS)


def reload_api_settings(*args, **kwargs):
    global api_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "AI_SUPPORT_SETTINGS":
        api_settings = APISettings(value, DEFAULTS)


setting_changed.connect(reload_api_settings)


import json
import hashlib
import hmac
import time

from django import template
from django.conf import settings


register = template.Library()


@register.inclusion_tag("intercom/_intercom_js.html")
def intercom_js(user):
    if hasattr(settings, "INTERCOM_APP_ID") and user.is_authenticated():
        if hasattr(settings, "INTERCOM_USER_HASH_KEY"):
            user_hash = hmac.new(settings.INTERCOM_USER_HASH_KEY, str(user.pk), hashlib.sha256).hexdigest()
        else:
            user_hash = None

        custom_data = {}
        for app in getattr(settings, "INTERCOM_APPS", []):
            m = __import__(app + ".intercom", globals(), locals(), ["intercom"])
            custom_data.update(m.custom_data(user))

        return {
            "app_id": settings.INTERCOM_APP_ID,
            "email": user.email,
            "user_hash": user_hash,
            "user": user,
            "created_at": int(time.mktime(user.date_joined.timetuple())),
            "custom_data": json.dumps(custom_data, ensure_ascii=False)
        }
    else:
        return {}

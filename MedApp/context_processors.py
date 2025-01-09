
from django.conf import settings


def site_info(request):
    return {
        'USERNAME': settings.USERNAME,
    }
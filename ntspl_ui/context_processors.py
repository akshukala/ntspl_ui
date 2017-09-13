from django.conf import settings

def service_urls(request):
    return {
        'user_service_url': settings.USER_SERVICE_URL,
        'local_url': settings.LOCAL_URL
        }

from .models import PageView
from django.utils import timezone

class PageViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Exclude admin and static paths
        if not request.path.startswith('/admin/') and not request.path.startswith('/static/'):
            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            PageView.objects.create(
                url=request.path,
                user=request.user if request.user.is_authenticated else None,
                ip_address=ip,
                method=request.method,
                timestamp=timezone.now()
            )

        return response

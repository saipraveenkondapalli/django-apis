from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Site


class ApiDomainCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.path.startswith("/api") or settings.DEBUG:
            return

        request_domain = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER') or request.META.get(
            'HTTP_HOST')

        client_id = request.GET.get('site') or request.META.get('X-SITE-ID')

        if not request_domain:
            return HttpResponse('Domain origin missing in headers', status=400)

        if not client_id:
            return HttpResponse("site key missing. place in query params as 'site' or in header as 'X-SITE-ID'",
                                status=400)

        site = get_object_or_404(Site, client_id=client_id)

        if site.url != request_domain:
            print(site.url, request_domain)
            return HttpResponse('Domain not allowed', status=400)

from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import Contact, Site
from .serializers import ContactSerializer


# Create your views here.


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_permissions(self):
        if self.action == 'create':
            permissions_classes = [permissions.AllowAny]
        else:
            permissions_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permissions_classes]

    def create(self, request, *args, **kwargs):
        request_domain = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER')

        if not request_domain:
            return Response({'message': 'Domain not allowed'}, status=400)

        site = Site.objects.get(client_id=request.data['site'])

        if site.url != request_domain:
            return Response({'message': 'Domain not allowed', "domain": request_domain}, status=400)

        return super().create(request, *args, **kwargs)

        # try:
        #     send_mail(
        #         'New Contact Form Submission',
        #         f'Name: {request.data["name"]}\nEmail: {request.data["email"]}\nMessage: {request.data["message"]}',
        #         settings.EMAIL_HOST_USER,
        #         [settings.EMAIL_HOST_USER],
        #     )
        #     print(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        #     return Response({'message': 'We have received your message. We will get back to you soon.'})
        #
        # except Exception as e:
        #     return response

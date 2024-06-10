from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resume, Site
from .serializers import ContactSerializer


class ContactCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        request_domain = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER')

        if not request_domain:
            return Response({'message': 'Domain not allowed'}, status=status.HTTP_400_BAD_REQUEST)

        site = get_object_or_404(Site, client_id=request.data['site'])

        if site.url != request_domain:
            return Response({'message': 'Domain not allowed', "domain": request_domain},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


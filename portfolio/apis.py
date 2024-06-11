from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resume
from .serializers import ContactSerializer, ResumeApiParamSerializer


class ContactCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeApiView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = ResumeApiParamSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        site = serializer.validated_data.get('site')
        key = serializer.validated_data.get('key')

        resume = get_object_or_404(Resume, site=site, key=key)

        return redirect(resume.url)

    def get_view_name(self):
        return 'Resume API View'

    def get_view_description(self, html=False):
        return 'This view is used to fetch resume url.'

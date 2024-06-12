from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resume, JobApplication
from .serializers import ContactSerializer, ResumeApiParamSerializer, JobApplicationMessageSerializer


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


class JobApplicationMessageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = JobApplicationMessageSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        message_id = serializer.validated_data.get('message_id')

        job_application = JobApplication.objects.filter(message_id=message_id).values(
            'title',
            'company',
            'url',
            'message',
            'notes'
        ).annotate(resume=F('resume__url'))

        if not job_application:
            return Response({'message': 'Job Application not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'data': job_application}, status=status.HTTP_200_OK)

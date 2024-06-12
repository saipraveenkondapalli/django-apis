from django.urls import path

from .apis import ContactCreateAPIView, ResumeApiView, JobApplicationMessageAPIView

urlpatterns = [
    path('contact/', ContactCreateAPIView.as_view(), name='contact'),
    path('resume/', ResumeApiView.as_view(), name='resume'),
    path('job-application-message/', JobApplicationMessageAPIView.as_view(), name='job-application-message'),

]

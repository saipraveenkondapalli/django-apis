from django.urls import path

from .apis import ContactCreateAPIView, ResumeApiView
from .views import dashboard

urlpatterns = [
    path('api/contact/', ContactCreateAPIView.as_view(), name='contact'),
    path('api/resume/', ResumeApiView.as_view(), name='resume'),
    path('dashboard/', dashboard, name='dashboard')
]

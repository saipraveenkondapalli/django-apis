from django.urls import path

from .apis import ContactCreateAPIView
from .views import dashboard

urlpatterns = [
    path('api/', ContactCreateAPIView.as_view(), name='contact'),
    path('dashboard/', dashboard, name='dashboard')
]

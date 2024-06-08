from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apis import ContactViewSet
from .views import dashboard

router = DefaultRouter()
router.register(r'contact', ContactViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', dashboard, name='dashboard')
]

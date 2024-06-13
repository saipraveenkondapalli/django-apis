from django.urls import path

from .views import SiteView, SiteDeleteView

app_name = 'portfolio'

urlpatterns = [
    path('dashboard/', SiteView.as_view(), name='dashboard'),
    path('portfolio/site/<uuid:pk>', SiteDeleteView.as_view(), name='delete_site'),
]

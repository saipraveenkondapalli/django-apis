from django.urls import path

from .views import SiteView, SiteDeleteView, SiteCreateView

app_name = 'portfolio'

urlpatterns = [
    path('dashboard/', SiteView.as_view(), name='dashboard'),
    path('portfolio/site/<uuid:pk>', SiteDeleteView.as_view(), name='delete_site'),
    path('portfolio/site/', SiteCreateView.as_view(), name='create_site'),
]

from django.urls import path

from .views import SiteView, SiteDeleteView, SiteCreateView, ContactView, SiteUpdateView

app_name = 'portfolio'

urlpatterns = [
    path('dashboard/', SiteView.as_view(), name='dashboard'),
    path('portfolio/site/<uuid:pk>', SiteDeleteView.as_view(), name='delete_site'),
    path('portfolio/site/', SiteCreateView.as_view(), name='create_site'),
    path('portfolio/contacts/', ContactView.as_view(), name='contacts'),
    path('portfolio/site/update/<uuid:pk>', SiteUpdateView.as_view(), name='update_site'),
]

from django.urls import path

from .views import dashboard

app_name = 'portfolio'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),

]

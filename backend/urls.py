from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Portfolio Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('portfolio.api_urls')),
    path('', include('portfolio.urls'))

]

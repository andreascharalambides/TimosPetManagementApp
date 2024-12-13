"""
URL configuration for TimosProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from users.views import service_worker

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pets.urls")),
    path("users/", include("users.urls")),
    path('logs/', include('logs.urls')),

path('static/js/service-worker.js', service_worker, name='service_worker'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Pet Management Admin'
admin.site.site_title = 'Pet Management Portal'
admin.site.index_title = 'Welcome to the Pet Management Admin Portal'

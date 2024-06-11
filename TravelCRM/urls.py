

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import re_path
from .views import CustomLoginView


urlpatterns = [
    re_path("media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path("static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("admin/", admin.site.urls),
    path("", include("Admin.urls")),
    path("",CustomLoginView,name="login"),
   
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

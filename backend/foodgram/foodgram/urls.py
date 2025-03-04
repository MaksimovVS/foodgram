# foodgram/urls.py

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from foodgram import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

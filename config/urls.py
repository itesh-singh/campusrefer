"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="CampusRefer API",
        default_version="v1",
        description="API for CampusRefer — alumni mentorship and referral platform",
    ),
    public=True,
    permission_classes=[AllowAny],
)

admin.site.site_header = "CampusRefer Admin"
admin.site.site_title = "CampusRefer Admin Portal"
admin.site.index_title = "Platform Management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin-panel/", include("adminpanel.urls")),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("students/", include("students.urls")),
    path("alumni/", include("alumni.urls")),
    path("connections/", include("connections.urls")),
    path("jobs/", include("jobs.urls")),
    path("dashboard/", include("dashboards.urls")),
    path("messages/", include("messaging.urls")),

    # REST API
    path("api/", include("api.urls")),

    # API Docs
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-docs"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-docs"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
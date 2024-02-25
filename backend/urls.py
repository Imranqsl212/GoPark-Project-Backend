from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from django.conf.urls.static import static
from django.conf import settings


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="GoPark API",
        default_version="1.0.0",
        description="API documentation of App",
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("user_auth.urls")),
    path(
        "docs/swagger/schema/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name='schema-swagger-ui',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# css and js for gunicorn
urlpatterns += staticfiles_urlpatterns()

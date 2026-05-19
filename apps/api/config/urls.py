from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.accounts.bootstrap_views import BootstrapCompleteTutorialStepView, BootstrapView

api_v1 = [
    path("auth/", include("apps.accounts.urls")),
    path("bootstrap/", BootstrapView.as_view(), name="bootstrap"),
    path("bootstrap/complete-tutorial-step/", BootstrapCompleteTutorialStepView.as_view(), name="bootstrap-complete-tutorial-step"),
    path("", include("apps.machines.urls")),
    path("", include("apps.filesystem.urls")),
    path("", include("apps.software.urls")),
    path("", include("apps.hardware.urls")),
    path("", include("apps.jobs.urls")),
    path("", include("apps.economy.urls")),
    path("", include("apps.networking.urls")),
    path("", include("apps.browser.urls")),
    path("", include("apps.marketplace.urls")),
    path("", include("apps.communications.urls")),
    path("", include("apps.progression.urls")),
    path("telemetry/", include("apps.telemetry.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/v1/", include(api_v1)),
]


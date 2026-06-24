# api/core_apps/infrastructure/health/views.py
from __future__ import annotations

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.infrastructure.health.services import HealthService
from core_apps.infrastructure.health.types import HealthCheckKind


class BaseHealthView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]
    health_kind: HealthCheckKind = "full"

    def get(self, request):
        if not getattr(settings, "HEALTH_CHECKS_ENABLED", True):
            return Response(
                {"detail": "Health checks are disabled."},
                status=404,
            )

        service = HealthService()
        report = self.get_report(service)
        status_code = 200 if report.status == "ok" else 503
        response = Response(report.as_dict(), status=status_code)

        # Health endpoints are intended for load balancers and orchestrators.
        # Keep the payload direct while preserving snake_case everywhere.
        response.skip_envelope = True
        return response

    def get_report(self, service: HealthService):
        if self.health_kind == "liveness":
            return service.liveness()
        if self.health_kind == "readiness":
            return service.readiness()
        return service.full()


class HealthView(BaseHealthView):
    health_kind = "full"


class LivenessHealthView(BaseHealthView):
    health_kind = "liveness"


class ReadinessHealthView(BaseHealthView):
    health_kind = "readiness"

from __future__ import annotations

from core_apps.common.limits.service import LimitContext, LimitService


class LimitViewMixin:
    limit_service_class = LimitService

    def get_limit_service(self) -> LimitService:
        return self.limit_service_class()

    def get_limit_config(self):
        getter = getattr(self.get_queryset().model, "get_limit_config", None)
        return getter() if callable(getter) else None

    def get_limit_context(self) -> LimitContext:
        return LimitContext(
            user=self.request.user,
            parent_id=self.get_limit_parent_id(),
            scope_id=self.get_limit_scope_id(),
        )

    def get_limit_parent_id(self) -> str | None:
        return (
            self.kwargs.get("parent_id")
            or self.request.data.get("parent")
            or self.request.query_params.get("parent")
        )

    def get_limit_scope_id(self) -> str | None:
        return (
            self.kwargs.get("scope_id")
            or self.request.data.get("scope")
            or self.request.query_params.get("scope")
        )

    def get_limits_snapshot(self):
        config = self.get_limit_config()

        if not config:
            return None

        return self.get_limit_service().get_snapshot(
            model=self.get_queryset().model,
            queryset=self.get_queryset(),
            config=config,
            context=self.get_limit_context(),
        )

    def get_limits_payload(self):
        snapshot = self.get_limits_snapshot()
        return snapshot.to_dict() if snapshot else None

    def finalize_response(self, request, response, *args, **kwargs):
        if 200 <= getattr(response, "status_code", 500) < 300:
            if getattr(response, "limits", None) is None:
                response.limits = self.get_limits_payload()

        return super().finalize_response(request, response, *args, **kwargs)

    def perform_create(self, serializer):
        snapshot = self.get_limits_snapshot()

        if snapshot:
            self.get_limit_service().assert_can_create(snapshot)

        serializer.save(created_by=self.request.user)

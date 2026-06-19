from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core_apps.common.constants import NAME_MIN_LENGTH
from core_apps.common.normalizers import normalize_human_name

NAME_ALLOWED_RE = re.compile(r"^[\w\s\-.,:;()/#&+áéíóúÁÉÍÓÚñÑüÜ]+$")


def validate_name_rules(value: str) -> None:
    normalized = normalize_human_name(value)

    if not normalized:
        raise ValidationError(_("The name cannot be blank."), code="blank")

    if len(normalized) < NAME_MIN_LENGTH:
        raise ValidationError(
            _("The name must contain at least %(min_length)s characters."),
            code="min_length",
            params={"min_length": NAME_MIN_LENGTH},
        )

    if normalized[0].isdigit():
        raise ValidationError(
            _("The name cannot start with a number."),
            code="starts_with_number",
        )

    if not NAME_ALLOWED_RE.fullmatch(normalized):
        raise ValidationError(
            _("The name contains unsupported characters."),
            code="invalid_characters",
        )

from __future__ import annotations

import factory
from django.contrib.auth import get_user_model

from core_apps.accounts.choices import UserRole
from tests.support.accounts.auth.payloads import DEFAULT_TEST_PASSWORD, unique_email


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    email = factory.LazyFunction(unique_email)
    first_name = "Factory"
    last_name = "User"
    role = UserRole.STUDENT
    is_active = True
    is_staff = False

    @factory.post_generation
    def password(self, create: bool, extracted: str | None, **kwargs) -> None:
        raw_password = extracted or DEFAULT_TEST_PASSWORD
        self.set_password(raw_password)

        if create:
            self.save(update_fields=["password"])


__all__ = ["UserFactory"]

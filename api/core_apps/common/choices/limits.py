from django.db import models
from django.utils.translation import gettext_lazy as _


class LimitStrategy(models.TextChoices):
    USER = "user", _("User")
    PARENT = "parent", _("Parent")
    GLOBAL = "global", _("Global")
    TREE = "tree", _("Tree")


class LimitFailureReason(models.TextChoices):
    LIMIT_REACHED = "limit_reached", _("Limit reached")
    TREE_DEPTH_REACHED = "tree_depth_reached", _("Tree depth reached")

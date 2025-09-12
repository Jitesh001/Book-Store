from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractTrack(models.Model):
    uuid = models.UUIDField(_("uuid field"), unique=True, default=uuid4, editable=False)
    created = models.DateTimeField(_("created at"), auto_now_add=True)
    modified = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True

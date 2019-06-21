from django.db import models

from wine.util import MAX_UNIQUE_CHARFIELD


class Partner(models.Model):
    """
    A Partner - e.g. Winemag.
    """
    name = models.CharField(max_length=256, null=False, blank=False)
    slug = models.CharField(max_length=MAX_UNIQUE_CHARFIELD, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name

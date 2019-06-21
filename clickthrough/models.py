from django.db import models
from django.db.models import CASCADE, PROTECT

from partners.models import Partner
from wine.models import MerchantWine


class Clickthrough(models.Model):
    """
    Each time a user clicks through our buy links we'll log it here.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    partner = models.ForeignKey(Partner, on_delete=CASCADE)
    # deleting a merchantwine probably shouldn't delete all clicks without a warning
    merchant_wine = models.ForeignKey(MerchantWine, on_delete=PROTECT)

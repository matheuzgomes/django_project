from django.db import models
from .user_information_model import UserInformations

class UserAccount(models.Model):
    account_type = models.CharField(max_length=50, default="Spot")
    available_amount = models.DecimalField(max_digits=6, decimal_places=2)
    loan_amount = models.DecimalField(max_digits=6, decimal_places=2)
    locked_amount = models.DecimalField(max_digits=6, decimal_places=2)
    user_id = models.ForeignKey(
        UserInformations,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

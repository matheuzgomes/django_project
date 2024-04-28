import uuid
from django.db import models

class UserInformations(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_info = models.CharField(max_length=300)
    user_password = models.CharField(max_length=500, null=True)
    national_id = models.CharField(max_length=200, null=True, blank=True)


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
 
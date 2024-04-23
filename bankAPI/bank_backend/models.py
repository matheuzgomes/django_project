import uuid
from django.db import models

class UserAccount(models.Model):
    available_amount = models.DecimalField(max_digits=6, decimal_places=2)
    locked_amount = models.DecimalField(max_digits=6, decimal_places=2)

class UserInfo(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_info = models.CharField(max_length=300)
    national_id = models.CharField(max_length=200, null=True, blank=True)
    user_account = models.ForeignKey(
        UserAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
 
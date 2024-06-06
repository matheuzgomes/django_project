import uuid
from django.db import models

class UserInformations(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_info = models.CharField(max_length=300)
    user_password = models.CharField(max_length=500, null=True)
    national_id = models.CharField(max_length=200, null=True, blank=True)


from django.contrib import admin
from .models import UserAccount, UserInformations

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserInformations)

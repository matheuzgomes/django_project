from django.contrib import admin
from .models import UserAccount, UserInfo

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserInfo)
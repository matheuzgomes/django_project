# Generated by Django 5.0.4 on 2024-04-21 00:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_backend', '0002_rename_user_id_useraccount_user_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='user_id',
            field=models.UUIDField(auto_created=True, default=uuid.UUID('14c275f0-22bb-4aff-8acf-672d4437b670'), primary_key=True, serialize=False, unique=True),
        ),
    ]

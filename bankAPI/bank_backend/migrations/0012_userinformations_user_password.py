# Generated by Django 5.0.4 on 2024-04-28 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_backend', '0011_useraccount_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformations',
            name='user_password',
            field=models.CharField(max_length=500, null=True),
        ),
    ]

# Generated by Django 2.2.1 on 2019-05-04 11:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_auto_20190504_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='user',
            field=models.ForeignKey(null=True, on_delete=models.SET(None), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='translation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=models.SET(None), to=settings.AUTH_USER_MODEL),
        ),
    ]
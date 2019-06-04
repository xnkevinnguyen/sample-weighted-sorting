# Generated by Django 2.0.2 on 2019-06-04 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_api', '0002_storeitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeitem',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='storeitem',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='storeitem',
            name='store_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='store_items', to=settings.AUTH_USER_MODEL),
        ),
    ]
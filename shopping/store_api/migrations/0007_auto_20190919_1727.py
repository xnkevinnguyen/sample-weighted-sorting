# Generated by Django 2.0.2 on 2019-09-19 17:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store_api', '0006_auto_20190606_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeitem',
            name='item_id',
            field=models.CharField(default=uuid.UUID('c895c108-b11d-43d3-94ad-633fb5738c88'), max_length=255, primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 2.0.2 on 2019-06-02 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_api', '0012_auto_20190602_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidateprofile',
            name='formation',
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='candidateprofile',
            name='schedule',
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='commercial_category',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='hiring_number',
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='office_number',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]

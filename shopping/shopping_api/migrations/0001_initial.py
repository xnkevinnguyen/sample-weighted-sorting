# Generated by Django 2.0.2 on 2019-06-01 20:17

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('first_name', models.CharField(default='', max_length=30)),
                ('last_name', models.CharField(default='', max_length=30)),
                ('phone_number', models.CharField(default='1112223333', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '5143339994'. between 9-15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('birth_date', models.CharField(default='20000101', max_length=8, validators=[django.core.validators.RegexValidator(message="Birthdate must be entered in the format: 'YYYY-MM-DD'", regex='^\\+?1?\\d{8}$')])),
                ('formation', models.IntegerField(default=0)),
                ('postal_code', models.CharField(default='XXXYYY', max_length=6, validators=[django.core.validators.RegexValidator(message='Length has to be 6', regex='^.{6}$')])),
                ('instagram_url', models.CharField(blank=True, max_length=100, validators=[django.core.validators.URLValidator(message='This is not a valid url.')])),
                ('specialities', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[0], size=None)),
                ('schedule', models.IntegerField(default=0)),
                ('availability_date', models.CharField(default='Now', max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

# Generated by Django 5.1.7 on 2025-05-07 01:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='artisanprofile',
            name='service',
            field=models.ManyToManyField(blank=True, to='core.service'),
        ),
        migrations.AddField(
            model_name='artisanprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artisanprofile',
            name='availability',
            field=models.ManyToManyField(to='accounts.availabilityoption'),
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='followed_tags',
            field=models.ManyToManyField(blank=True, to='core.tag'),
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='preferred_categories',
            field=models.ManyToManyField(blank=True, to='core.category'),
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='otpverification',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

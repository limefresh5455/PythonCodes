# Generated by Django 4.1.7 on 2023-07-19 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_customuser_active_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='financialStatus',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='mortgageAmount',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='mortgageType',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='propertyLocation',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='propertyType',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='propertyValue',
            field=models.TextField(default=''),
        ),
    ]

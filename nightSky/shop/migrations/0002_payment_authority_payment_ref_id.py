# Generated by Django 4.0.3 on 2022-03-26 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='authority',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='payment',
            name='ref_id',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]

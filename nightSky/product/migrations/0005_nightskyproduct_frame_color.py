# Generated by Django 4.0.3 on 2022-03-24 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_nightskyproduct_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='nightskyproduct',
            name='frame_color',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]

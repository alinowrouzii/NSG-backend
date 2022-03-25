# Generated by Django 4.0.3 on 2022-03-25 10:15

from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256)),
                ('image', models.ImageField(upload_to=product.models.get_color_path)),
            ],
        ),
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256)),
                ('image', models.ImageField(upload_to=product.models.get_design_path)),
            ],
        ),
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=256)),
                ('image', models.ImageField(upload_to=product.models.get_font_path)),
            ],
        ),
        migrations.CreateModel(
            name='MapDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=256)),
                ('image', models.ImageField(upload_to=product.models.get_map_design_path)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='NightSkyProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentense', models.CharField(blank=True, max_length=512)),
                ('handwriting', models.CharField(blank=True, max_length=512)),
                ('location', models.CharField(blank=True, max_length=512)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('qr_code', models.CharField(blank=True, max_length=512)),
                ('map', models.CharField(blank=True, max_length=512)),
                ('sound_frequency', models.CharField(blank=True, max_length=512)),
                ('is_shiny', models.BooleanField(default=False)),
                ('frame_color', models.CharField(blank=True, max_length=512)),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='night_sky_products', to='product.color')),
                ('design', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='night_sky_products', to='product.design')),
                ('font', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='night_sky_products', to='product.font')),
                ('map_design', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='night_sky_products', to='product.mapdesign')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='night_sky_product', to='product.model')),
                ('size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='night_sky_product', to='product.size')),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='product_model', serialize=False, to='product.model')),
                ('sizes', models.ManyToManyField(to='product.size')),
            ],
        ),
    ]

from django.db import models
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver


main_dir = "product"
color_dir = "color"
design_dir = "design"
map_design_dir = "map_design"
font_dir = "font_design"


def get_color_path(instance, filename):
    return os.path.join(main_dir, color_dir, filename)


def get_design_path(instance, filename):
    return os.path.join(main_dir, design_dir, filename)


def get_map_design_path(instance, filename):
    return os.path.join(main_dir, map_design_dir, filename)


def get_font_path(instance, filename):
    return os.path.join(main_dir, font_dir, filename)


class Color(models.Model):
    text = models.CharField(max_length=256, blank=True)
    image = models.ImageField(upload_to=get_color_path, blank=False, null=False)


class Design(models.Model):
    text = models.CharField(max_length=256, blank=True)
    image = models.ImageField(upload_to=get_design_path, blank=False, null=False)


class MapDesign(models.Model):
    text = models.CharField(max_length=256, blank=True)
    image = models.ImageField(upload_to=get_map_design_path, blank=False, null=False)


class Font(models.Model):
    text = models.CharField(max_length=256, blank=True)
    image = models.ImageField(upload_to=get_font_path, blank=False, null=False)


class Size(models.Model):
    size = models.CharField(max_length=256, blank=False, null=False)


class Model(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)


class ProductModel(models.Model):
    model = models.OneToOneField("product.Model", on_delete=models.CASCADE)
    sizes = models.ManyToManyField("product.Size")


class NightSkyProduct(models.Model):
    color = models.ForeignKey(
        "product.Color", on_delete=models.DO_NOTHING, related_name="night_sky_products"
    )
    design = models.ForeignKey(
        "product.Design", on_delete=models.DO_NOTHING, related_name="night_sky_products"
    )
    font = models.ForeignKey(
        "product.Font", on_delete=models.DO_NOTHING, related_name="night_sky_products"
    )
    map_design = models.ForeignKey(
        "product.MapDesign", on_delete=models.DO_NOTHING, related_name="night_sky_products"
    )
    sentense = models.CharField(max_length=512, blank=True)
    handwriting = models.CharField(max_length=512, blank=True)
    location = models.CharField(max_length=512, blank=True)

    date = models.DateTimeField(blank=True)
    qr_code = models.CharField(max_length=512, blank=True)
    map = models.CharField(max_length=512, blank=True)
    sound_frequency = models.CharField(max_length=512, blank=True)
    is_shiny = models.BooleanField(default=False)
    model = models.ForeignKey(
        "product.Model", on_delete=models.DO_NOTHING, related_name="night_sky_product"
    )
    size = models.ForeignKey(
        "product.Size", on_delete=models.DO_NOTHING, related_name="night_sky_product"
    )
    # size = models.In


@receiver(pre_save, sender=NightSkyProduct)
def my_callback(sender, instance, *args, **kwargs):
    # Reverse relation from model to OneToOne field
    model = instance.model.model
    if not instance.size in model.sizes.all():
        return ValidationError({"model_size": "size does not exist for selected model"})

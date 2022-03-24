from django.contrib import admin
from product.models import (
    Color,
    Design,
    MapDesign,
    Font,
    Model,
    Size,
    ProductModel,
    NightSkyProduct,
)

# Register your models here.


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("id", "text")


@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ("id", "text")


@admin.register(MapDesign)
class MapDesignAdmin(admin.ModelAdmin):
    list_display = ("id", "text")


@admin.register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display = ("id", "text")



@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("id", "size")
    
@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "get_model_name")
    
    @admin.display(description='model name')
    def get_model_name(self, obj):
        return obj.model.name


@admin.register(NightSkyProduct)
class NightSkyProduct(admin.ModelAdmin):
    list_display = ("id", "get_model_name", "get_color")
    
    @admin.display(description='model name')
    def get_model_name(self, obj):
        return obj.model.name
    
    @admin.display(description='color')
    def get_color(self, obj):
        return obj.color.text
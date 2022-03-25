from django.contrib import admin
from django.forms import ModelForm, ValidationError
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
    list_display = ("get_id", "get_model_name")

    
    @admin.display(description="id")
    def get_id(self, obj):
        return obj.model.id

    @admin.display(description="model name")
    def get_model_name(self, obj):
        return obj.model.name


class NightSkyProductAdminForm(ModelForm):
    class Meta:
        model = NightSkyProduct
        fields = "__all__"

    def clean(self):
        cleaned_data = self.cleaned_data
        
        model = cleaned_data.get("model")
        product_size = cleaned_data.get("size")
        if model and product_size:
            try:
                if not product_size in model.product_model.sizes.all():
                    raise ValidationError("This size is not exist for specified model!")
            except ProductModel.DoesNotExist:
                raise ValidationError(f"ProductModel with {model.name} model name does not exist.")
            
        return cleaned_data


@admin.register(NightSkyProduct)
class NightSkyProduct(admin.ModelAdmin):
    list_display = ("id", "get_model_name", "get_color")

    form = NightSkyProductAdminForm

    @admin.display(description="model name")
    def get_model_name(self, obj):
        return obj.model.name

    @admin.display(description="color")
    def get_color(self, obj):
        return obj.color.text

from rest_framework import serializers
from product.models import (
    Color,
    Font,
    Design,
    MapDesign,
    ProductModel,
    Size,
    Model,
    NightSkyProduct,
)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class FontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Font
        fields = "__all__"


class DesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Design
        fields = "__all__"


class MapDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapDesign
        fields = "__all__"


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = "__all__"


class ProductModelSerializer(serializers.ModelSerializer):
    model = ModelSerializer(read_only=True)
    sizes = SizeSerializer(read_only=True, many=True)
    class Meta:
        model = ProductModel
        fields = ("model", "sizes")


class NightSkyProductSerializer(serializers.ModelSerializer):
    color = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(),
        write_only=False,
        required=True,
    )

    font = serializers.PrimaryKeyRelatedField(
        queryset=Font.objects.all(),
        write_only=False,
        required=True,
    )
    design = serializers.PrimaryKeyRelatedField(
        queryset=Design.objects.all(),
        write_only=False,
        required=True,
    )

    map_design = serializers.PrimaryKeyRelatedField(
        queryset=MapDesign.objects.all(),
        write_only=False,
        required=True,
    )

    size = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(),
        write_only=False,
        required=True,
    )

    model = serializers.PrimaryKeyRelatedField(
        queryset=Model.objects.all(),
        write_only=False,
        required=True,
    )

    def to_representation(self, obj):
        self.fields["color"] = ColorSerializer()
        self.fields["font"] = FontSerializer()
        self.fields["design"] = DesignSerializer()
        self.fields["map_design"] = MapDesignSerializer()
        self.fields["size"] = SizeSerializer()
        self.fields["model"] = ModelSerializer()

        return super(NightSkyProductSerializer, self).to_representation(obj)

    class Meta:
        model = NightSkyProduct
        fields = (
            "color",
            "font",
            "design",
            "map_design",
            "size",
            "model",
            "sentense",
            "handwriting",
            "location",
            "date",
            # TODO check qr_code needs to be fill by user or admin
            "qr_code",
            "map",
            "sound_frequency",
            "is_shiny",
            "frame_color",
        )
        extra_kwargs = {
            "sentense": {"write_only": False},
            "handwriting": {"write_only": False},
            "location": {"write_only": False},
            "date": {"write_only": False},
            "qr_code": {"read_only": True},
            "map": {"write_only": False},
            "sound_frequency": {"write_only": False},
            "is_shiny": {"write_only": False},
            "frame_color": {"write_only": False, "required": True},
        }

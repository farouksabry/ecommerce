from rest_framework import serializers
from .models import Product, Store, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]

class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(write_only=True)
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    images = serializers.ListField(child=serializers.ImageField(), allow_empty=True, max_length=10, write_only=True, required=False)
    product_images = ProductImageSerializer(source="images", many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "store", "in_stock", "stock", "images", "product_images"]
        read_only_fields = ["in_stock"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context["request"].user.is_authenticated and not self.context["request"].user.is_staff:
            self.fields["store"].queryset = Store.objects.filter(
                owner__user=self.context["request"].user
            )

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        product = Product.objects.create(**validated_data)

        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return product

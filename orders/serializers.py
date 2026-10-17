from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "status", "unit_price"]
        read_only_fields = ["order", "unit_price"]

    def validate_product(self, data):
        if not data.in_stock:
            raise serializers.ValidationError(f"{data.name} is out of stock.")
        return data

    def validate(self, data):
        if self.instance:
            if self.instance.order.user == self.context["request"].user:
                if any(field != "quantity" for field in data):
                    raise serializers.ValidationError("You can only update quantity.")

                if data["quantity"] > (self.instance.quantity + self.instance.product.stock):
                    raise serializers.ValidationError(f"{self.instance.product.name} doesn't have your requested quantity right now.")

            elif self.instance.product.store.owner.user == self.context["request"].user:
                if any(field != "status" for field in data):
                    raise serializers.ValidationError("You can only update status.")
        else:
            if data["quantity"] > data["product"].stock:
                raise serializers.ValidationError(f"Only {data['product'].stock} items are available for product {data['product'].name}.")

        return data

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return sum(
            item.item_subtotal for item in obj.items.all()
        )

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "updated_at", "address", "mobile", "paid", "payment_method", "items", "total_price"]
        read_only_fields = ["user", "created_at", "updated_at", "paid", "total_price"]

    def create(self, validated_data):
        items = validated_data.pop("items")
        mobile = validated_data.pop("mobile", None)
        user = self.context["request"].user

        with transaction.atomic():
            order = Order.objects.create(user=user, mobile= mobile if mobile else user.mobile, **validated_data)

            for item in items:
                OrderItem.objects.create(order=order, product=item["product"], quantity=item["quantity"], unit_price=item["product"].price)
                item["product"].stock -= item["quantity"]
                item["product"].save()
        return order

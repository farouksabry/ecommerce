from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Merchant, Store
from accounts.serializers import UserSerializer

User = get_user_model()
        
class MerchantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Merchant
        fields = ["id", "user"]

class MerchantCreationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Merchant
        fields = ["user"]

    def create(self, validated_data):
        user = self.context["request"].user

        if Merchant.objects.filter(user=user).exists():
            raise serializers.ValidationError({"error": "Merchant already exists."})

        return Merchant.objects.create(user=user)

class StoreSerializer(serializers.ModelSerializer):
    owner = MerchantSerializer(read_only=True)

    class Meta:
        model = Store
        fields = ["id", "name", "owner", "open_date"]
        read_only_fields = ["open_date"]

    def create(self, validated_data):
        return Store.objects.create(owner=self.context["request"].user.merchant, **validated_data)

class AdminStoreCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "owner"]

    def create(self, validated_data):
        return Store.objects.create(**validated_data)

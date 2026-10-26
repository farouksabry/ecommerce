from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'dob', 'mobile', 'country']

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password', 'password2', 'dob', 'gender', 'mobile', 'country']
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise serializers.ValidationError({"Password Confirmation": "Passwords do not match!"})

        try:
            password_validation.validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"Password": e.messages})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        return get_user_model().objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if data["new_password"] != data["new_password2"]:
            raise serializers.ValidationError({"Password Confirmation": "Passwords do not match!"})

        try:
            password_validation.validate_password(data["new_password"], self.context["request"].user)
        except ValidationError as e:
            raise serializers.ValidationError({"Password": e.messages})
        return data

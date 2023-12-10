from rest_framework import serializers
from .models import MyUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email
        token["is_admin"] = user.is_superuser
        token["created_date"] = user.created_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        return token


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
        }

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "username", "email", "created_date", "is_superuser")


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

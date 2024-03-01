from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Ride, RideApplication


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class RideApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer()

    class Meta:
        model = RideApplication
        fields = "__all__"


class RideSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    applications = RideApplicationSerializer(many=True, read_only=True)

    start_time = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = Ride
        fields = "__all__"

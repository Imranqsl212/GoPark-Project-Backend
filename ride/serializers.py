from rest_framework import serializers
from django.conf import settings
from .models import Ride, RideApplication
from datetime import datetime


class RideApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideApplication
        fields = "__all__"


class RideSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    applications = RideApplicationSerializer(many=True, read_only=True)

    start_time = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = Ride
        fields = "__all__"


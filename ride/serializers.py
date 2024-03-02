from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Ride, RideApplication
from datetime import datetime

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

    def validate(self, data):
        if 'start_time' in self.context['request'].query_params:
            start_time = self.context['request'].query_params['start_time']
            try:
                datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                raise serializers.ValidationError("Invalid start time format. Use ISO 8601 format.")
        return data

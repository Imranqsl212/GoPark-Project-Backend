from django.db import models
from django.contrib.auth import get_user_model


class Ride(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    expected_time_hours = models.PositiveIntegerField()
    additional_comment = models.TextField()
    max_applicants = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Ride from {self.from_location} to {self.to_location}"


class RideApplication(models.Model):
    ride = models.ForeignKey(
        Ride, on_delete=models.CASCADE, related_name="applications"
    )
    applicant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    waiting_location = models.CharField(max_length=100)
    is_driver = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.applicant.username} applied for {self.ride}"

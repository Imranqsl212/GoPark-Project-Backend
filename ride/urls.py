from django.urls import path
from .views import *


urlpatterns = [
    path("rides/", get_all_rides, name="get_all_rides"),
    path("rides/<int:ride_id>/", get_ride, name="get_ride"),
    path("rides/create/", create_ride, name="create_ride"),
    path("rides/update/<int:ride_id>/", update_ride, name="update_ride"),
    path("rides/delete/<int:ride_id>/", delete_ride, name="delete_ride"),
]

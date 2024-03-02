from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Ride
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, F


class CustomRidesPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 1000


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_ride(request):
    serializer = RideSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_rides(request):
    rides = Ride.objects.annotate(num_applicants=Count("applications")).filter(
        num_applicants__lt=F("max_applicants")
    )
    paginator = CustomRidesPagination()
    result_page = paginator.paginate_queryset(rides, request)
    serializer = RideSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = RideSerializer(ride)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_for_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if ride.applications.count() >= ride.max_applicants:
        return Response(
            {"detail": "Ride is already full"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = RideApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(ride=ride, applicant=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if ride.owner != request.user:
        return Response(
            {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )

    serializer = RideSerializer(ride, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if ride.owner != request.user:
        return Response(
            {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )

    ride.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_rides(request):
    start_time = request.query_params.get('start_time', None)
    max_applicants = request.query_params.get('max_applicants', None)

    if start_time:
        rides = Ride.objects.filter(start_time__gte=start_time)

    if max_applicants:
        rides = Ride.objects.filter(max_applicants__gte=max_applicants)

    if not start_time and not max_applicants:
        rides = Ride.objects.all()

    paginator = CustomRidesPagination()
    result_page = paginator.paginate_queryset(rides, request)
    serializer = RideSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

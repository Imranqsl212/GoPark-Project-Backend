import django_filters
from .models import Ride

class RideFilter(django_filters.FilterSet):
    from_location = django_filters.CharFilter(field_name='from_location', lookup_expr='icontains')
    to_location = django_filters.CharFilter(field_name='to_location', lookup_expr='icontains')
    start_time_gte = django_filters.DateTimeFilter(field_name='start_time', lookup_expr='gte')
    start_time_lte = django_filters.DateTimeFilter(field_name='start_time', lookup_expr='lte')
    max_applicants_gte = django_filters.NumberFilter(field_name='max_applicants', lookup_expr='gte')

    class Meta:
        model = Ride
        fields = ['from_location', 'to_location', 'start_time_gte', 'start_time_lte', 'max_applicants_gte']
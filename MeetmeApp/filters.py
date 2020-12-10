import django_filters
from django_filters import CharFilter, NumericRangeFilter, RangeFilter
from .models import *


class UserFilter(django_filters.FilterSet):
    name = CharFilter(field_name="full_name", lookup_expr="icontains")
    gender = CharFilter(field_name="gender")
    career = CharFilter(field_name="career", lookup_expr='icontains')
    age = RangeFilter(field_name="age")

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user", 'profile_image', 'bio', 'career',
                   'full_name', 'age', 'gender', 'likeability', 'blocked_by']

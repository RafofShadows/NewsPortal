
from django_filters import FilterSet, DateFilter, CharFilter

from .forms import DateInput, DateTimeInput
from .models import Post


class PostFilter(FilterSet):
    name = CharFilter(field_name='header', lookup_expr='icontains')
    category = CharFilter(field_name='categories__name', lookup_expr='iexact')
    post_date = DateFilter(field_name='timestamp', lookup_expr='gt',
                           widget=DateInput(format='%d.%m.%Y')
                           )

    class Meta:
        fields = {
            'name',
            'category',
            'post_date',
        }


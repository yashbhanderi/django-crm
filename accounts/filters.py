from sqlite3 import Date
import django_filters
from .models import *
from django_filters import DateFilter, CharFilter
from django.forms.widgets import TextInput

class OrderFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name='date_created', lookup_expr='gte', label='Start Date', 
    widget = TextInput(attrs={'placeholder': 'dd/mm/yyyy'}))
    end_date = DateFilter(field_name='date_created', lookup_expr='lte', label='End Date', widget = TextInput(attrs={'placeholder': 'dd/mm/yyyy'}))
    note = CharFilter(field_name='note', lookup_expr='icontains', label='note')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']
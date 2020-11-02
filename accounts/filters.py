from django.forms.widgets import TextInput
import django_filters

from django_filters import CharFilter
from django.forms.widgets import TextInput
from .models import *


class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',
                      lookup_expr='icontains', label='', 
                      widget=TextInput(attrs={'class':'form-control-sm', 
                      'placeholder': 'Search product...',
                      'autocomplete': 'off'}))

    class Meta:
        model = Product
        fields = ['name']


class CustomerFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',
                      lookup_expr='icontains',label='',
                      widget=TextInput(attrs={'class':'form-control-sm',
                      'placeholder':'Search customer...',
                      'autocomplete': 'off'}))

    class Meta:
        model = Customer
        fields = ['name']
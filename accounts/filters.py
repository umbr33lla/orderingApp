from django.forms import widgets
from django.forms.widgets import TextInput
import django_filters

from django_filters import CharFilter
from django.forms.widgets import TextInput
from .models import *


class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',
                      lookup_expr='icontains', label='', widget=TextInput(attrs={'placeholder': 'Search product...'}))

    class Meta:
        model = Product
        fields = ['name']

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm, TextInput
from .models import Customer, Product


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']
        labels = {
            'name': _('Product')
        }
        widgets = {
            'name': TextInput(attrs={'autocomplete': 'off'})
        }







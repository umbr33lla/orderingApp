from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import Customer


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CreateCustomerForm(ModelForm):
    class  Meta:
        model = Customer
        fields = '__all__'




from django.forms import ModelForm
from .models import Sales, SaleDetails, Customers
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomerForm(ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'
        exclude = ['user', 'customer_id']


class SalesForm(ModelForm):
    class Meta:
        model = Sales
        fields = ['sale_id', 'customer_id', 'status']


class SaleDetailsForm(ModelForm):
    class Meta:
        model = SaleDetails
        fields = ['product', 'quantity']
        exclude = ('sale',)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.fields.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.fields.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.fields.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.fields.TextInput(attrs={'placeholder': 'Email-address'}),
        }
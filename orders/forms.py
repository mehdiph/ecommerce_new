from django import forms
from .models import Order
from .models import Shipping


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
        }

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = [
            'shipping_duration',
            'address',
            'postal_code',
            'city',
        ]

        widgets = {
            'shipping_duration': forms.Select(attrs={
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
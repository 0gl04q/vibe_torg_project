from django import forms

from apps.orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'price']
        labels = {
            'status': '',
            'price': '',
        }

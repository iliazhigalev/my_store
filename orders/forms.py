from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ринат'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Усманов'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Россия, Москва, ул. Мира, дом 6'}
                                       ),
        }

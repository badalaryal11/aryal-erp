from django import forms
from django.forms import inlineformset_factory
from .models import Sale, SaleItem

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name', 'payment_method']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }

SaleItemFormSet = inlineformset_factory(
    Sale, SaleItem,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=True,
    widgets={
        'product': forms.Select(attrs={'class': 'form-select'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
    }
)

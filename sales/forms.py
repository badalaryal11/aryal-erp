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

from django.forms import BaseInlineFormSet

class BaseSaleItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                product = form.cleaned_data.get('product')
                quantity = form.cleaned_data.get('quantity')
                
                if product and quantity:
                    if quantity > product.stock_quantity:
                        excess = quantity - product.stock_quantity
                        form.add_error('quantity', f"Insufficient Quantity in inventory. Exceeded by {excess}. Available: {product.stock_quantity}")

SaleItemFormSet = inlineformset_factory(
    Sale, SaleItem,
    formset=BaseSaleItemFormSet,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=True,
    widgets={
        'product': forms.Select(attrs={'class': 'form-select'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
    }
)

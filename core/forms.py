from django import forms
from .models import Sale, Product, Store

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['date', 'store', 'product', 'quantity']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full rounded-lg border-gray-300'}),
            'store': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300'}),
            'product': forms.Select(attrs={'class': 'w-full rounded-lg border-gray-300'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full rounded-lg border-gray-300', 'min': '1'}),
        }
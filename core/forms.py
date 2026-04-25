from django import forms
from .models import Sale, Product, Store, Competition

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['store', 'product', 'quantity']
        labels = {
            'store': 'Κατάστημα',
            'product': 'Προϊόν',
            'quantity': 'Ποσότητα (Τεμάχια)',
        }
        widgets = {
            'store': forms.Select(attrs={'class': 'rounded-xl border-gray-200 focus:ring-blue-500 w-full'}),
            'product': forms.Select(attrs={'class': 'rounded-xl border-gray-200 focus:ring-blue-500 w-full'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'rounded-xl border-gray-200 focus:ring-blue-500 w-full',
                'min': '1',
                'placeholder': 'Π.χ. 5'
            }),
        }

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['store', 'comments']
        labels = {
            'store': 'Κατάστημα',
            'comments': 'Σχόλια / Παρατηρήσεις',
        }
        widgets = {
            'store': forms.Select(attrs={
                'class': 'rounded-xl border-gray-200 focus:ring-blue-500 w-full'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'rounded-xl border-gray-200 focus:ring-blue-500 w-full',
                'rows': 5,
                'placeholder': 'Π.χ. Ο ανταγωνιστής X έβαλε προσφορά 1+1 στο προϊόν Y...'
            }),
        }
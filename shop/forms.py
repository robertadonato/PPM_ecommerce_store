from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    cc_name = forms.CharField(label="Nome sulla carta", max_length=100)
    cc_number = forms.CharField(label="Numero carta", max_length=19)
    cc_expiry = forms.CharField(label="Scadenza", max_length=5)
    cc_cvv = forms.CharField(label="CVV", max_length=3)
        
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=12, help_text="Format: 2547XXXXXXXX")
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'postal_code', 'city']

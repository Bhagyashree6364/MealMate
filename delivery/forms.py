from django import forms
from .models import UserProfile, Order

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['number', 'delivery_address']  # Include other fields if your model has more

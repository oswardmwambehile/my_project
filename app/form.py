from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'country', 'mobile', 'zipcode', 'city']  # Exclude 'user' from here

    # Custom widgets for other fields
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
        'placeholder': 'Full Name',
    }))

    locality = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
        'placeholder': 'Locality',
    }))
    
    country = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
        'placeholder': 'Country',
    }))

    mobile = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
        'placeholder': 'Mobile Number',
    }))

    zipcode = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
        'placeholder': 'Zipcode',
    }))

    city = forms.ChoiceField(choices=Customer.STATE_CHOICE, widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
    }))






class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        })
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        })
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        label='Email',
    )

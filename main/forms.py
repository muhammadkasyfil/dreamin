from django import forms
from django.contrib.auth.models import User

# Signup Form
class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'w-full bg-white/20 border border-white/30 text-white placeholder-white/70 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-softpink',
        'placeholder': 'Enter your username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full bg-white/20 border border-white/30 text-white placeholder-white/70 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-softpink',
        'placeholder': 'Enter your email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full bg-white/20 border border-white/30 text-white placeholder-white/70 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-softpink',
        'placeholder': 'Enter your password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full bg-white/20 border border-white/30 text-white placeholder-white/70 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-softpink',
        'placeholder': 'Confirm your password'
    }))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data
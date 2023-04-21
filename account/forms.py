from django import forms
from .models import CustomUser, Profile
from django.core.validators import EmailValidator


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserRegisterationForm(forms.Form):
    email = forms.EmailField(label='Email', validators=[EmailValidator])
    phone_number = forms.CharField(max_length=11, label='Phone Number')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password Confirmation')
    email.widget.attrs['class'] = 'form-control'
    phone_number.widget.attrs['class'] = 'form-control'


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()

    code.widget.attrs['class'] = 'form-control'

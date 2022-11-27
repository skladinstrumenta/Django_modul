from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from Eshop.models import MyUser, Purchase, Product


class UserCreateForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)
    deposit = forms.DecimalField(initial=10000, widget=forms.HiddenInput)

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'password2', 'deposit')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered')
        return email


class PurchaseCreateForm(forms.ModelForm):
    amount = forms.IntegerField()

    class Meta:
        model = Purchase
        fields = ['amount']


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'text', 'price', 'image', 'amount')

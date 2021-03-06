from django import forms
from .models import Client
from django.contrib.auth import get_user_model


class ClientRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Client
        fields = ["username", "password", "email",
                  "fullname", "phone", "adress", "city"]

    # verifier si username entré par l'user deja existe
    def clean_username(self):
        User = get_user_model()
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Sorry, that username's taken. Try another?")
        return username


class ClientLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class CheckoutForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Fullname"}), required=True)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': "xxx@xxx.xxx"}))
    adress = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Address"}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "+212 XXXXXXXX"}))
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "City"}))
    zipcode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ex: 20100"}))

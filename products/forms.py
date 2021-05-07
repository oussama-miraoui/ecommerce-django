from django import forms
from .models import Client
from django.contrib.auth.models import User


class ClientRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Client
        fields = ["username", "password", "email",
                  "fullname", "phone", "adress", "city"]

    # verifier si username entré par l'user deja existe
    # ça marche pas!
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(
                u'Username "%s" is already in use.' % username)
        return username


class ClientLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class CheckoutForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Fullname"}), required=True)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username"}))
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
    payment_options = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

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
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError(
    #             f'Username {username} is already in use, try another one.')
    #     return username


class ClientLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

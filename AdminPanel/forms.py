from AdminPanel.models import Admin
from django.contrib.auth import(authenticate, get_user_model, login, logout)
from django import forms
from django.db.models.fields.related import ForeignKey
from django.forms.fields import MultipleChoiceField
from products.models import *


class ProductForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'class': 'form-control imginp', 'type': 'file'}))

    class Meta:
        model = Produit
        fields = ['nom', 'categorie', 'description',
                  'image', 'ancienPrix', 'prix', 'stock']
        widgets = {
            'nom':   forms.TextInput(attrs={'class': 'form-control'}),
            'categorie':   forms.Select(attrs={'class': 'form-control'}),
            'description':   forms.Textarea(attrs={'class': 'form-control'}),
            'ancienPrix':   forms.NumberInput(attrs={'class': 'form-control'}),
            'prix':   forms.NumberInput(attrs={'class': 'form-control'}),
            'stock':   forms.NumberInput(attrs={'class': 'form-control'})
        }


class CategorieForm(forms.ModelForm):

    class Meta:
        model = Categorie
        fields = "__all__"
        widgets = {
            'nom':   forms.TextInput(attrs={'class': 'form-control'}),
            'description':   forms.Textarea(attrs={'class': 'form-control'}),

        }


class userForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Admin
        fields = ["username", "password", "email", "fullname"]
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'password':   forms.Select(attrs={'class': 'form-control'}),
            'email':   forms.Textarea(attrs={'class': 'form-control'}),
            'fullname':   forms.TextInput(attrs={'class': 'form-control'})

        }

    # verifier si username entré par l'user deja existe

    def clean_username(self):
        User = get_user_model()
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Sorry, that username's taken. Try another?")
        return username

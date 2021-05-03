from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([Produit, Categorie, Client,
                     Couleur, Taille, Detail_Produit, Panier, ])

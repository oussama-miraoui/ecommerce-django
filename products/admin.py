from AdminPanel.models import Admin
from django.contrib import admin
from products.models import *

# Register your models here.

admin.site.register([LigneCommande,user,Produit, Admin,Categorie, Client,
                     Couleur, Taille, Detail_Produit, Panier, Paiement, Commande])

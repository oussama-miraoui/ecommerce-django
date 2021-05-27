from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(User(), on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    adress = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.fullname


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to="images")
    ancienPrix = models.PositiveIntegerField(blank=True, null=True)
    prix = models.PositiveIntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.nom


class Taille(models.Model):
    taille = models.CharField(max_length=20)

    def __str__(self):
        return self.taille


class Couleur(models.Model):
    couleur = models.CharField(max_length=50)

    def __str__(self):
        return self.couleur


class Detail_Produit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    couleur = models.ForeignKey(
        Couleur, on_delete=models.CASCADE, blank=True, null=True)
    taille = models.ForeignKey(
        Taille, on_delete=models.CASCADE, blank=True, null=True)


class Panier(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    couleur = models.CharField(max_length=50, blank=True, null=True)
    taille = models.CharField(max_length=40, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    def subTotal(self):
        return self.quantity * self.produit.prix


class Paiement(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, blank=True, null=True)
    montant = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client.fullname


class Commande(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    produits = models.CharField(max_length=200, default='PRODUIT')
    methode_paiment = models.CharField(max_length=20, blank=True, null=True)
    paiement = models.ForeignKey(
        Paiement, on_delete=models.SET_NULL, blank=True, null=True)
    etat = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return self.client.fullname

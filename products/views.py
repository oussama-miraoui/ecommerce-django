from typing import Tuple
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, CreateView, FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from products.forms import ClientRegistrationForm, ClientLoginForm, CheckoutForm
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import LigneCommande, Produit, Categorie, Detail_Produit, Panier, Paiement, Commande
import stripe
from django.db.models import F

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductsView(View):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'

    def get(self, request):
        # get all products
        products = Produit.objects.all()
        # get all categories
        categories = Categorie.objects.all()

        try:
            # get the query string from url parameter
            getCategorie = request.GET.get('categorie')
            # get the value of search the input
            searchValue = request.GET.get('q')
        except:
            getCategorie = None
            searchValue = None

        # check if getCategorie equal the name of categorie
        if getCategorie:
            # filter by categorie
            categorie = get_object_or_404(Categorie, nom=getCategorie)
            products = products.filter(categorie=categorie)
        elif searchValue:
            # _contains est comme 'like' dans sql
            products = Produit.objects.filter(nom__icontains=searchValue)
        else:
            products = Produit.objects.all().order_by('nom')

        context = {"products": products,
                   "categories": categories,
                   "search": searchValue
                   }
        return render(
            request,
            "products/products.html",
            context
        )


class ProductView(View):
    def get(self, request, id):
        product = Produit.objects.get(id=id)
        # get the product details
        product_detail = Detail_Produit.objects.all()
        # get the product details by product ID
        details = product_detail.filter(produit_id=id)

        return render(request, "products/product.html", {"product": product, "details": details})

# LoginRequiredMixin => l'user n'accède pas a la page sauf qu'il est authentifié


class CartView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get(self, request):
        # get all from panier where client_id = Client.id
        client_panier = Panier.objects.filter(
            client_id=request.session['user_id'])
        request.session['count_panier'] = client_panier.count()
        return render(request, "cart/cart.html", {"paniers": client_panier, "count": request})


class OrdersView(View):
    def get(self, request):
        orders = Commande.objects.all().order_by('-date_commande')
        # get all from panier where client_id = Client.id
        client_order = orders.filter(client_id=request.session['user_id'])

        # commandes = Commande.objects.all()
        # lignes = LigneCommande.objects.all()

        return render(request, "orders.html", {"orders": client_order})


class CheckoutView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get(self, request):
        # initial => set default values for form fields
        form = CheckoutForm(initial={
            'fullname': request.user.client.fullname,
            'username': request.user.username,
            'email': request.user.email,
            'phone': request.user.client.phone,
            'email': request.user.email,
            'adress': request.user.client.adress,
            'city': request.user.client.city
        })

        paniers = Panier.objects.filter(client_id=request.session['user_id'])

        return render(request, "checkout.html", {'form': form, "paniers": paniers})

    def post(self, *args, **kwargs):
        paniers = Panier.objects.filter(
            client_id=self.request.session['user_id'])
        total = 0
        listProduits = ""

        for panier in paniers:
            total += panier.subTotal()
            Produit.objects.filter(id=panier.produit.id).update(
                stock=F('stock') - panier.quantity)
            # les produits commandés par le client et ses quantités
            #listProduits += f" {panier.produit.nom} x{panier.quantity}."

        token = self.request.POST.get('stripeToken')
        # print(token)

        charge = stripe.Charge.create(
            amount=total * 50,
            currency="MAD",
            source=token
        )

        # creer le paiement
        paiement = Paiement()
        paiement.stripe_charge_id = charge['id']
        paiement.client = self.request.user.client
        paiement.montant = total
        paiement.save()

        # creer la commande
        commande = Commande()
        commande.client = self.request.user.client
        commande.methode_paiment = "Stripe"
        commande.paiement = paiement
        commande.Total = total
        commande.save()

        for panier in paniers:
            Ligne_Com = LigneCommande()
            Ligne_Com.Commande = commande
            Ligne_Com.Produit = panier.produit
            Ligne_Com.Qte = panier.quantity
            Ligne_Com.save()
        # vider le panier
        paniers.delete()

        messages.success(
            self.request, f"Your order was submitted! check your ")
        return redirect('checkout')


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = ClientRegistrationForm
    success_url = reverse_lazy("register")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        User = get_user_model()

        user = User.objects.create_user(username, email, password)
        # Setting user as a client
        User.objects.filter(pk=user.pk).update(is_client=True)

        form.instance.user = user

        # afficher un message de success si le client est inscrit.
        messages.info(self.request, "You've registered, go to ")

        return super().form_valid(form)


class LoginView(FormView):
    template_name = "login.html"
    # import the form from forms.py
    form_class = ClientLoginForm
    # redirect
    # success_url = reverse_lazy("login")

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        pwd = form.cleaned_data['password']

        user = authenticate(username=uname, password=pwd)

        if user is not None:
            login(self.request, user)
            # store the user id in session
            self.request.session['user_id'] = self.request.user.client.id

            # get the parameter 'redirect_to' from url to redirect the user after login
            if 'redirect_to' in self.request.GET:
                return redirect(self.request.GET.get('redirect_to'))
        else:
            messages.error(self.request, "Username or password invalid.")
            return render(self.request, self.template_name, {"form": self.form_class})

        return redirect('products')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('products')


# CART operations

@login_required(login_url='/login/')
def addToCart(request):
    if request.method == 'POST':
        # get the query string from url parameter
        taille = request.POST.get('size')
        couleur = request.POST.get('color')
        quantite = request.POST.get('quantity')
        id_produit = request.POST.get('id-p')
        total = request.POST.get('total')
        if taille or couleur or quantite or id_produit or total:
            # check if the client already added the same product to the cart and update its quantity
            if Panier.objects.filter(produit_id=id_produit, client_id=request.session['user_id']).exists():
                messages.success(
                    request, "Quantity updated!")
                item = get_object_or_404(Panier,
                                         produit_id=id_produit, client_id=request.session['user_id'])
                item.quantity += 1
                item.save()
                return redirect('cart')
            else:
                panier = Panier(client_id=request.session['user_id'],
                                produit_id=id_produit,
                                couleur=couleur,
                                taille=taille,
                                total=total,
                                subtotal=total,
                                quantity=quantite)

                panier.save()
                messages.success(request, "Item added!")
        # Redirect to the same page
        return redirect('cart')

    return redirect('cart')


def removeFromCart(request):
    if request.method == "POST":
        id_produit = request.POST.get('id-p')

        if id_produit and request.session['user_id']:
            panier = Panier.objects.filter(
                produit_id=id_produit, client_id=request.session['user_id'])
            panier.delete()
            messages.success(request, "Item deleted!")
            return redirect("cart")


def removeItemFromCart(request):
    if request.method == 'POST':
        id_produit = request.POST.get('id-p')

        if id_produit and request.session['user_id']:
            item = get_object_or_404(
                Panier, produit_id=id_produit, client_id=request.session['user_id'])
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                messages.success(request, "Quantity updated!")
            else:
                removeFromCart(request)
            return redirect("cart")


def emptyCart(request):
    panier = Panier.objects.filter(client_id=request.session['user_id'])
    panier.delete()
    return redirect("cart")

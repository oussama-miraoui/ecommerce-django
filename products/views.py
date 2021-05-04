from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView, CreateView, FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import ClientRegistrationForm, ClientLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Produit, Categorie, Detail_Produit, Panier

# Create your views here.


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
            products = Produit.objects.all()

        context = {"products": products,
                   "categories": categories,
                   "search": searchValue
                   }
        return render(
            request,
            "products/products.html",
            context
        )

# LoginRequiredMixin => l'user n'accède ppas a la page sauf qu'il est authentifié


class ProductView(View):
    def get(self, request, id):
        product = Produit.objects.get(id=id)
        # get the product details
        product_detail = Detail_Produit.objects.all()
        # get the product details by product ID
        details = product_detail.filter(produit_id=id)

        return render(request, "products/product.html", {"product": product, "details": details})


class AboutView(TemplateView):
    # login_url = '/login/'
    # redirect_field_name = "redirect_to"
    template_name = "about.html"


class CartView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get(self, request):
        paniers = Panier.objects.all()
        # get all from panier where client_id = Client.id

        client_panier = paniers.filter(client_id=request.user.client.id)
        return render(request, "cart/cart.html", {"paniers": client_panier})


class OrdersView(TemplateView):
    template_name = "orders.html"


class CheckoutView(TemplateView):
    template_name = "checkout.html"


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = ClientRegistrationForm
    success_url = reverse_lazy("register")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        # afficher un message de success si le client est inscrit.
        messages.add_message(self.request, messages.INFO,
                             f"You've registered, go to ")
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "login.html"
    # import the form from forms.py
    form_class = ClientLoginForm
    # redirect
    success_url = reverse_lazy("login")

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


def addToCart(request):
    if request.method == 'POST':
        # get the query string from url parameter
        taille = request.POST.get('size')
        couleur = request.POST.get('color')
        quantite = request.POST.get('quantity')
        id_produit = request.POST.get('id-p')
        total = request.POST.get('total')
        if taille or couleur or quantite or id_produit or total:
            # check if the client already added the same product to the cart
            if Panier.objects.filter(produit_id=id_produit, client_id=request.session['user_id']).exists():
                messages.error(request, "Item already exist!")
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
        #Redirect to the same page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def removeFromCart(request):
    if request.method == "POST":
        id_produit = request.POST.get('id-p')

        if id_produit and request.session['user_id']:
            panier = Panier.objects.filter(produit_id=id_produit, client_id=request.session['user_id'])
            panier.delete()
            messages.success(request, "Item deleted!")
            return redirect("cart")


def emptyCart(request):
    panier = Panier.objects.filter(client_id=request.session['user_id'])
    panier.delete()
    return redirect("cart")

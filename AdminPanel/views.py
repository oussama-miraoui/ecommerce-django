import products
from django import views
from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.contrib.messages.api import error
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .decorators import anonyme_user
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.views.generic import ListView, CreateView
from products.models import *
from django.shortcuts import get_object_or_404
from AdminPanel.forms import *
from products.models import user as us
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.utils.decorators import method_decorator


class Home(View):
    def get(self, request):

        return render(request, "AdminTEMPLATES/Home.html")


class ProduitListView(View):
    def get(self, request):
        # get all products
        products = Produit.objects.all()
        # get all categories
        categories = Categorie.objects.all()

        try:
            # get the query string from url parameter
            getCategorie = request.GET.get('categorie')
            # get the value of search the input
            searchValue = request.GET.get('search')
        except:
            getCategorie = None
            searchValue = None

        # check if getCategorie = the name of categorie
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
            "AdminTEMPLATES/Produit.html",
            context
        )


def Alogin_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('productList')

        else:
            messages.error(request, 'username or password not correct')
            return render(request, 'AdminTEMPLATES/registration/Login.html', {'form': form})

    else:
        form = AuthenticationForm()

    if request.user.is_authenticated:
        return redirect('productList')

    return render(request, 'AdminTEMPLATES/registration/Login.html', {'form': form})


@anonyme_user
def Create_Product(request):

    if request.method == 'POST':

        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()

            return redirect('productList')
        else:
            context = {'product': form, 'messages': form.errors}
            return render(request, "Create_Product.html", context)

    else:
        form = ProductForm()
        context = {'product': form, 'messages': form.errors}
        return render(request, "AdminTEMPLATES/Create_Product.html", context)


class Edit_Product(View):

    def get(self, request, id):
        product = Produit.objects.get(id=id)
        form = ProductForm(instance=product)

        return render(request, 'AdminTEMPLATES/ProductEdit.html', {'form': form})

    def post(self, request, id):
        product = Produit.objects.get(id=id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('productList')
        else:

            context = {'product': form, 'messages': form.errors}
            return render(request, 'AdminTEMPLATES/ProductEdit.html', context)


def Delete_Product(request, id):

    if request.method == 'GET':
        product = Produit.objects.filter(id=id)

        product.delete()

        return redirect('productList')


def logout_view(request):
    logout(request)
    return redirect('adminLogin')


def Forbiden(request):

    return render(request, "AdminTEMPLATES/notAllowed.html")


class CategorieListView(View):

    def get(self, request, id=None):
        categorieForm = CategorieForm()
        categories = Categorie.objects.all()
        # For update in same page
        if id is not None:
            categorie = Categorie.objects.get(id=id)
            categorieForm = CategorieForm(instance=categorie)

        return render(
            request,
            "AdminTEMPLATES/categorie.html",
            {"categories": categories, "form": categorieForm}
        )

    def post(self, request, id=None):
        # Update Same page--
        if id is not None:
            categorie = Categorie.objects.get(id=id)
            categorieForm = CategorieForm(request.POST, instance=categorie)
            if categorieForm.is_valid():
                categorieForm.save()
                return redirect('categorieList')
        else:
            # Create
            categorieForm = CategorieForm(request.POST)
            if categorieForm.is_valid():
                categorieForm.save()
            return redirect('categorieList')


def Delete_Category(request, id):

    if request.method == 'GET':
        Cat = Categorie.objects.filter(id=id)

        Cat.delete()

        return redirect('categorieList')


# @login_required(login_url='/Admin/login')


class CommandeListView(View):
    def get(self, request, *args, **kwargs):
        # makhedmatch
        # cmd=Commande.objects.get(id=1)
        # cmd.LigneCommande_set.all()

        Commandes = Commande.objects.all().order_by('-date_commande')
        Ligne = LigneCommande.objects.all()

        context = {
            'Commandes': Commandes,
            'LigneCommande': Ligne
        }
        return render(request, "AdminTEMPLATES/Commande.html", context)


def EtatCommande(request, Commande_id):
    if request.method == 'GET':

        Commande.objects.filter(id=Commande_id).update(etat="Traitée")

    return redirect('Commande')


def DeleteCommande(request, Commande_id):
    if request.method == 'GET':

        Commande.objects.filter(id=Commande_id).delete()

    return redirect('Commande')


class RegisterViewA(CreateView):
    template_name = "AdminTEMPLATES/registration/register.html"
    form_class = userForm
    success_url = reverse_lazy("Aregister")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        User = get_user_model()

        user = User.objects.create_user(username, email, password)
        # Setting user as a client
        User.objects.filter(pk=user.pk).update(is_admin=True)

        form.instance.user = user

        # afficher un message de success si le client est inscrit.
        messages.info(self.request, "Admin added succesfully.")

        return super().form_valid(form)


class AdminListView(View):

    def get(self, request, *args, **kwargs):

        Admins = Admin.objects.all()

        context = {"Admins": Admins}
        return render(
            request,
            "AdminTEMPLATES/Admin.html",
            context
        )


def Delete_Admin(request, Admin_id):

    if request.method == 'GET':
        idp = Admin_id
        Cat = Admin.objects.filter(id=idp).delete()
    return redirect('AList')


def DashboardView(request):
    total = 0
    current_user = request.user
    User = user.objects.filter(id=current_user.id)
    Coms = Commande.objects.all()
    Non_t = Commande.objects.filter(etat="Non traitée").count()
    LigneCom = LigneCommande.objects.all()
    Prod = {}
    for Ligne in LigneCom:
        Ligne.Produit.id
        if Ligne.Produit.id in Prod:
            Prod[Ligne.Produit.id] += 1
        else:
            Prod = {Ligne.Produit.id: 1}
    max_key = max(Prod, key=Prod.get)

    BestSeller = Produit.objects.get(id=max_key)

    for Com in Coms:
        total = total+Com.Total
    context = {'User': User, 'total': total,
               'bestSell': BestSeller, 'Non_traite': Non_t}

    return render(request,
                  "AdminTEMPLATES/Dashboard.html",
                  context)

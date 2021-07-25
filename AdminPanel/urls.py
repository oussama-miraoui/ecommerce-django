from django.urls import path
from AdminPanel import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from .decorators import anonyme_user
urlpatterns = [



    path('Admin/home', anonyme_user(views.ProduitListView.as_view()),
         name="productList"),
    path('Admin/login', views.Alogin_view, name="adminLogin"),
    path('Admin/logout/', anonyme_user(views.logout_view), name="adminLogout"),
    path('Admin/Produit/Create',
         anonyme_user(views.Create_Product), name='createProduct'),
    path('Admin/Produit/Edit/<int:id>',
         anonyme_user(views.Edit_Product.as_view()), name='editProduct'),
    path('Admin/Produit/Delete/<int:id>',
         anonyme_user(views.Delete_Product), name='deleteProduct'),
    path('Admin/Category', anonyme_user(views.CategorieListView.as_view()),
         name='categorieList'),
    path('Admin/Category/Create',
         anonyme_user(views.Create_Product), name='createCategorie'),
    path('Admin/Category/Edit/<int:id>',
         anonyme_user(views.CategorieListView.as_view()), name='editCategorie'),
    path('Admin/Category/Delete/<int:id>',
         anonyme_user(views.Delete_Category), name='deleteCategorie'),
    path('Admin/Command', anonyme_user(views.CommandeListView.as_view()),
         name='Commande'),
    path('Admin/Command/Etat/<int:Commande_id>',
         anonyme_user(views.EtatCommande), name='CommandeEtat'),
    path('Admin/Command/Delete/<int:Commande_id>',
         anonyme_user(views.DeleteCommande), name='deleteCommande'),
    path('Admin/Register', anonyme_user(views.RegisterViewA.as_view()), name='Aregister'),
    path('Admin/AdminList', anonyme_user(views.AdminListView.as_view()), name='AList'),
    path('Admin/Admin/Delete/<int:Admin_id>',
         anonyme_user(views.Delete_Admin), name='AdminDel'),
    path('Forbiden', views.Forbiden, name='Forbiden'),
    path('Admin/Dashboard', anonyme_user(views.DashboardView), name='Dashboard')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

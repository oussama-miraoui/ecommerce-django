from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('', views.ProductsView.as_view(), name="products"),
    path('about/', views.AboutView.as_view(), name="about"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path('product/<int:id>', views.ProductView.as_view(), name="product"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('orders/', views.OrdersView.as_view(), name="orders"),
    path('add-to-cart/', views.addToCart, name="add-to-cart"),
    path('remove-from-cart/', views.removeFromCart, name="remove-from-cart"),
    path('empty-cart/', views.emptyCart, name="empty-cart"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
]
# BA9I MAFHEMTSH HAD LCODE !!!!!!!!!!!!!!!
# KI AFFICHER LINA TSSAWER DIAL LES PRODUITS
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

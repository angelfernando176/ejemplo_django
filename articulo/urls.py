from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_articulos, name='lista_articulos'),
    path('crear/', views.crear_articulo, name='crear_articulo'),
    path('editar/<int:pk>/', views.editar_articulo, name='editar_articulo'),
    path('eliminar/<int:pk>/', views.eliminar_articulo, name='eliminar_articulo'),
    path('api/json/', views.api_articulos_json, name='api_articulos_json'),
    path('api/stock-bajo/', views.api_stock_bajo_json, name='api_stock_bajo_json'),
]
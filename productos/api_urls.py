from django.urls import path
from . import api_views

app_name = 'productos_api'

urlpatterns = [
    path('productos/', api_views.ProductoListAPI.as_view(), name='products-list'),
    path('productos/<int:pk>/', api_views.ProductoDetailAPI.as_view(), name='products-detail'),
]

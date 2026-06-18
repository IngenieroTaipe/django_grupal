from rest_framework import generics
from .models import Producto
from .serializers import ProductoSerializer


class ProductoListAPI(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class ProductoDetailAPI(generics.RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

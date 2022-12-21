from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from Eshop.api.serializers import ProductSerializer
from Eshop.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
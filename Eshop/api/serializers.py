from rest_framework import serializers
from Eshop.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'text', 'price', 'amount']
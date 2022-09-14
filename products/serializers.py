from dataclasses import fields
from rest_framework import serializers
from accounts.serializers import UserSerializer

from products.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [            
            'id',
            'description',
            'seller',
            'price',
            'quantity',
            'is_active'
        ]
        read_only_fields = ['id', 'is_active', 'seller']

    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [            
            'id',
            'description',
            'seller',
            'price',
            'quantity',
            'is_active'
        ]
        read_only_fields = ['id', 'seller', 'description', 'price', 'quantity', 'is_active']




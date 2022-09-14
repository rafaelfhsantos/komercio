from rest_framework import generics, views, authentication, permissions

from .serializers import ProductSerializer ,ProductDetailSerializer
from .models import Product
from .permissions import IsSeller, IsOwnerSeller
from .mixins import SerializerByMethodMixin

from drf_spectacular.utils import extend_schema

class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsSeller]

    queryset = Product.objects.all()   

    serializer_map = {
        "GET": ProductSerializer,
        "POST": ProductDetailSerializer
    }    
    

    def perform_create(self, serializer):
        # import ipdb; ipdb.set_trace()
        serializer.save(seller=self.request.user) 
    

class ProductDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerSeller]

    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer    

    @extend_schema(exclude=True)
    def put():
        ...



from rest_framework import permissions
from rest_framework.views import Request, View

from products.models import Product


class IsSeller(permissions.BasePermission):
    def has_permission(self, request: Request, view: View): 
        
        if request.method in permissions.SAFE_METHODS:            
            return True  

        return hasattr(request.user,'is_seller') and request.user.is_seller or request.user.is_superuser



class IsOwnerSeller(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, product: Product): 
        
        if request.method in permissions.SAFE_METHODS:            
            return True   

        return hasattr(request.user,'is_seller') and request.user == product.seller or request.user.is_superuser
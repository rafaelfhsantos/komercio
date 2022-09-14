from rest_framework import permissions
from rest_framework.views import Request, View


class IsOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View): 
        
        if request.method in permissions.SAFE_METHODS:            
            return True   

        pk = view.kwargs.get('pk') 

        # import ipdb; ipdb.set_trace()        

        return ('is_active' not in request.data and request.user.id == pk) or request.user.is_superuser

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View): 
        return request.user.is_superuser


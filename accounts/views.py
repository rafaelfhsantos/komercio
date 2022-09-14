from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import authentication, permissions

from .serializers import UserSerializer, UserManagementSerializer
from .models import Account
from .permissions import IsOwner, IsAdmin

from drf_spectacular.utils import extend_schema

class UsersView(ListCreateAPIView):    
    queryset = Account.objects.all()
    serializer_class = UserSerializer

class NewestUsersView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):        
        return Account.objects.order_by('-date_joined')[:self.kwargs['num']]
    
class UserDetailView(UpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwner]
    
    queryset = Account.objects.all()
    serializer_class = UserSerializer

    @extend_schema(exclude=True)
    def put():
        ...

class UserManagementView(UpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdmin]
    
    queryset = Account.objects.all()
    serializer_class = UserManagementSerializer

    @extend_schema(exclude=True)
    def put():
        ...



from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Account


class UserSerializer(serializers.ModelSerializer):
    is_seller = serializers.BooleanField(required=True)

    class Meta:
        model = Account
        fields = [   
            'id',         
            'username',    
            'password',        
            'first_name',
            'last_name',
            'is_seller',
            'date_joined',
            'is_active',
            'is_superuser'
        ]
        read_only_fields = ['id','date_joined', 'is_active', 'is_superuser']        
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [   
            'id',         
            'username', 
            'first_name',
            'last_name',
            'is_seller',
            'date_joined',
            'is_active',
            'is_superuser'
        ]
        read_only_fields = [
            'username', 
            'first_name',
            'last_name',
            'is_seller',
            'date_joined',            
            'is_superuser'
            ] 
        
        
    
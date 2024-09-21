from djoser.serializers import UserCreateSerializer as BaseCreateUserSerializer , UserSerializer as BaseUserSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseCreateUserSerializer):
  # birth_date = serializers.DateField()
  
  class Meta(BaseCreateUserSerializer.Meta):
    fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
  class Meta(BaseUserSerializer.Meta):
    fields =['id','username', 'email', 'first_name', 'last_name']
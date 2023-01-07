from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    identity_no = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    verified = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

class LoginSerializer(serializers.Serializer):
    identity_no = serializers.CharField()
    password = serializers.CharField()
    

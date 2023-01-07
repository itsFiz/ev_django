from django.shortcuts import render

from users.serializers import UserSerializer,LoginSerializer
from users.models import User
from knox.models import AuthToken
from django.contrib.auth import authenticate

# Create your views here.

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from users.authentication import CustomAuthentication


@api_view(['POST'])
def resident_register(request):
    data = request.data

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    user = User.objects.create(
        identity_no=data['identity_no'],
        name=data['name'],
        email=data['email'],
        password=data['password'],
    )

    token = AuthToken.objects.create(user)

    user = UserSerializer(user)

    return Response(data={"user":user.data, "token": token[1]}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def resident_login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    user = User.objects.filter(identity_no=data['identity_no'], password=data['password']).first()

    if user is None:
        return Response(data={'message':'user not found'}, status=status.HTTP_401_UNAUTHORIZED)

    token = AuthToken.objects.create(user=user)

    user = UserSerializer(user)

    return Response(data={"user":user.data, "token": token[1]}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([CustomAuthentication,])
def resident_logout(request):
    user = request.user

    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            t = token.partition(" ")
            token = t[-1]

        if not token:
            return None

        token = token[:8]

        token = AuthToken.objects.filter(token_key=token).first()
        token.delete()

        return Response({'message':'success'})
    except Exception as e:
        return Response({'message':'failed'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([CustomAuthentication,])
def resident_logout_all(request):
    user = request.user

    try:
        AuthToken.objects.filter(user_id=user.id).delete()

        return Response({'message':'success'})
    except Exception as e:
        return Response({'message':'failed'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def admin_verify(request):

    try: 
        
        data = request.data

        if data['user_id'] is None or data['verified'] is None:
            return Response({'message':'failed'}, status=status.HTTP_412_PRECONDITION_FAILED)

        user = User.objects.filter(id=data['user_id']).first() 

        user.verified=data['verified']

        user.save()

        return Response({'message':'success'})

    except Exception as e: 
        print(e)
        return Response({'message':'failed'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_residents(request):

    users = User.objects.all()

    serializer = UserSerializer(users, many=True)
    
    return Response(data=serializer.data)
    
@api_view(['DELETE'])
def admin_delete(request):

    try: 
        
        data = request.data

        if data['user_id'] is None:
            return Response({'message':'failed'}, status=status.HTTP_412_PRECONDITION_FAILED)

        user = User.objects.filter(id=data['user_id']).first() 

        user.delete()

        return Response({'message':'success'})

    except Exception as e: 
        print(e)
        return Response({'message':'failed'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([CustomAuthentication,])
def get_user(request):

    try: 
        user = request.user

        serializer = UserSerializer(user)
    
        return Response(data={'user':serializer.data})

    except Exception as e:
        print(e)
        return Response({'message':'failed'}, status=status.HTTP_401_UNAUTHORIZED)

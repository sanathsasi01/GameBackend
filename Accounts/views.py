from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework import status
import requests
import json
from django.contrib.auth import get_user_model
User = get_user_model() 
# Create your views here.


@api_view(['POST'])
@permission_classes((AllowAny,))
def Registration(request):
    # to find the user type
    userSerializer = RegistrationSerializers(data=request.data)
    if userSerializer.is_valid():
        userSerializer.save()
        context = {
            "status_code" : 200,
            "Message" : "User has been successfully registered"
        }
        return JsonResponse(context, status=status.HTTP_200_OK)
    else:
        return JsonResponse(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes((AllowAny,))
def Login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        profile = RegistrationSerializers(user)

    else:
        return JsonResponse(serializer.errors)

    token, created = Token.objects.get_or_create(user=user)

    context = {
        'token' : token.key,
        'profile' : profile.data
    }

    return JsonResponse(context,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def Profile(request):
    user = request.user
    profile = RegistrationSerializers(user)

    return JsonResponse(profile.data, safe=False)



def resetPassword(request):
    token = request.GET.get('token','')
    context = {'token' : token}
    return render(request, 'pwd_reset/reset.html', context)



def setPassword(request):
    token = request.POST.get('token')
    password = request.POST.get('password')
    reset_endpoint = request.build_absolute_uri().replace('/password-change/', '/api/password_reset/confirm/')
    data = {
        'password' : password,
        'token' : token
    }
    headers = {'content-type': 'application/json'}
    try:
        result = requests.post(reset_endpoint,headers=headers, data=json.dumps(data))
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    json_result = json.loads(result.text)
    context = {
        'result' : json_result
    }
    return render(request, 'pwd_reset/successful.html',context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import login, authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import random
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from user.models import Profile, User, Mobile
from GlobalVariables import *
from .serializers import (MobileSerializer, RegisterMobileSerializer,
                        MobileVerifySerializer, UserSerializerWithToken)

class LoginUser(APIView):
    def get(self, request):
        return Response({"response":"success"})

@swagger_auto_schema(
    methods=["POST"],
    request_body = RegisterMobileSerializer,
    responses = {200: MobileSerializer}
)
@api_view(['POST'])
def registerMobile(request):
    data = request.data
    generated_code = random.randint(1000, 9999)
    data['sms_code'] = generated_code
    if Mobile.objects.filter(mobile=data['mobile']).exists():
        tMobile = Mobile.objects.filter(mobile=data['mobile']).first()
        tMobile.is_sms_sent = False
        tMobile.is_verified = False
        tMobile.save()
        serializer = MobileSerializer(tMobile)
        return Response({"response":"success", "message": SUCCESS_MESSAGE_MOBILE}, 
                        status=status.HTTP_200_OK)
    # try:
    serializer = MobileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.create(
            username = data["mobile"],
            password = make_password(serializer.data["sms_code"])
        )
        return Response({"response":"success", "message": SUCCESS_MESSAGE_MOBILE},
                        status=status.HTTP_201_CREATED)
    # except:
    #     return Response({"response":"error"}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=["GET"],
    responses = {200: MobileVerifySerializer}
)
@api_view(['GET'])
def smsList(request):
    tMobiles = Mobile.objects.filter(is_sms_sent=False)
    mobiles = tMobiles.filter(is_verified=False)
    for mobile in mobiles:
        mobile.is_sms_sent = True
        mobile.save()
    serializer = MobileVerifySerializer(mobiles, many=True)
    return Response({"response":"success", 'data':serializer.data})

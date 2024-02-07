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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from user.models import Profile, User, Mobile
from GlobalVariables import *
from .serializers import *

class LoginUser(APIView):
    @swagger_auto_schema(
        operation_summary="Login User",
        request_body = LoginInSerializer,
        responses={200: openapi.Response(
            description="Response Exapmle",
            examples={
                "application/json": {
                "response": "success",
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NDI1NzY4OSwiaWF0IjoxNjkxNjY1Njg5LCJqdGkiOiI2ZTEyOTkzNzhjN2Q0MTZjYTdkY2I2OWUzNjVhNDQ2ZCIsInVzZXJfaWQiOjN9.OTK0b1YSmf_YZdRcAEGx_H0hTap0QBMg7Tq4d1zbguc",
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzMjAxNjg5LCJpYXQiOjE2OTE2NjU2ODksImp0aSI6Ijg5MDI3NmFhY2MxZjQxZmM4ZjgyNTU0MWUzZDM5ZjIxIiwidXNlcl9pZCI6M30.P08T4zGldVZYhilroe60xrv7e60PC3RWn4UUwWp4POM",
                "user": {
                    "id": 3,
                    "username": "+99365346683",
                    "is_driver": True
                }
                }
            }
        )},
    )
    def post(self, request):
        data = request.data
        if 'password' in data:
            if data['password'] == None or data['password'] == "":
                return Response({
                        "response":"error",
                        "message": MSG_NO_PASSWORD,
                        }, status=status.HTTP_400_BAD_REQUEST)
            if 'username' not in data:
                return Response({
                    'response': "error", 
                    "message": MSG_NO_USER_INFO,
                    }, status=status.HTTP_400_BAD_REQUEST)
            password = data['password']
            username = data['username']
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({
                    "response":"error",
                    "message": MSG_USERNAME_OR_PASSWORD_ERROR,
                    "data": {}
                }, status=status.HTTP_404_NOT_FOUND)
        serializer = LoginOutSerializer(user)
        refresh = RefreshToken.for_user(user)
        return Response({
            "response":"success",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data,
        })
    
@swagger_auto_schema(
    methods=["POST"],
    request_body = RegisterMobileSerializer,
    responses = {200: MobileSerializer}
)
@api_view(['POST'])
def registerMobile(request):
    try:
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
        serializer = MobileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.create(
                username = data["mobile"],
                password = make_password(serializer.data["sms_code"])
            )
            return Response({"response":"success", "message": SUCCESS_MESSAGE_MOBILE},
                            status=status.HTTP_201_CREATED)
    except:
        return Response({"response":"error"}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=["GET"],
    responses = {200: MobileVerifySerializer}
)
@api_view(['GET'])
def smsList(request):
    tMobiles = Mobile.objects.filter(is_sms_sent=False, is_verified=False)
    for mobile in tMobiles:
        mobile.is_sms_sent = True
        mobile.save()
    serializer = MobileVerifySerializer(tMobiles, many=True)
    return Response({"response":"success", 'data':serializer.data})


class DriversList(APIView, LimitOffsetPagination):
    @swagger_auto_schema(
        operation_summary="Drivers List"
    )
    def get(self, request):
        drivers = User.objects.filter(is_driver=True)
        data = self.paginate_queryset(drivers, request, view=self)
        serializer = DriversListSerializer(data, many=True)
        results = self.get_paginated_response(serializer.data)
        return Response({
            "response":"success",
            "data":results.data
        }, status=status.HTTP_200_OK)

class DriverDetail(APIView):
    @swagger_auto_schema(
        operation_summary="Drivers List"
    )
    def get(self, request, pk):
        if User.objects.filter(pk=pk).exists():
            driver = User.objects.get(pk=pk)
            serializer = DriverDetailSerializer(driver)
            return Response({"response":"success", "data":serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"response": "error", "message":MSG_OBJECT_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)

class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="User Detail",
    )
    def get(self, request, pk):
        user = request.user
        if User.objects.filter(pk=pk).exists():
            if user != User.objects.get(pk=pk):
                return Response({"response":"error", "detail":MSG_NOT_BELONG_TO_USER})
            user_info = User.objects.get(pk=pk)
            serializer = UserOutSerializer(user_info)
            return Response({
                "response":"success",
                "data":serializer.data
            })
        else:
            return Response({
                "response":"error",
                "message": MSG_OBJECT_NOT_FOUND,
            }, status=status.HTTP_404_NOT_FOUND)
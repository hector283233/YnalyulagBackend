from rest_framework import serializers
from user.models import User, Profile, Mobile
from api.transport.serializers import TripDetailSrializer2, TripTransportOutSerializer

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = "__all__"
        
class RegisterMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ["mobile"]

class MobileVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ["mobile", "sms_code"]
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class LoginOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_driver"]

class LoginInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class DriversListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class DriverDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserOutSerializer(serializers.ModelSerializer):
    transports = TripTransportOutSerializer(source="user_transport", many=True)
    trips = TripDetailSrializer2(source="user_trip", many=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_driver", "transports", "trips"]
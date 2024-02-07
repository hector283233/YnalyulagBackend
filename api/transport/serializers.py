from rest_framework import serializers
from user.models import User
from transport.models import *

class LocationsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = "__all__"

class UserOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "last_login", "username", "is_driver", 
                  "email"]

class TransportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        exclude = ("is_active", )

class TransportOutSerializer(serializers.ModelSerializer):
    user = UserOutSerializer()
    class Meta:
        model = Transport
        fields = ["id", "model", "vehicle_type", "image",
                  "created_at", "user"]
        
class TripTransportOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ["id", "model", "vehicle_type", "image",
                  "created_at"]

class TripCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"

class TripOutSerializer(serializers.ModelSerializer):
    user = UserOutSerializer()
    transport_id = TripTransportOutSerializer()
    from_location = LocationsListSerializer()
    to_location = LocationsListSerializer()
    class Meta:
        model = Trip
        fields = ["id", "leaving_time", "capacity", "is_intercity", 
                  "is_onway", "description", "from_location",
                  "to_location", "user", "transport_id", "is_active",
                  "cargo", "passanger"]

class TripListSerializer(serializers.ModelSerializer):
    user = UserOutSerializer()
    transport_id = TripTransportOutSerializer()
    from_location = LocationsListSerializer()
    to_location = LocationsListSerializer()
    class Meta:
        model = Trip
        fields = ["id","leaving_time", "capacity", "is_intercity", 
                  "is_onway", "description", "from_location",
                  "to_location", "user", "transport_id", "is_active",
                  "cargo", "passanger"]

class TripDetailSrializer(serializers.ModelSerializer):
    user = UserOutSerializer()
    transport_id = TripTransportOutSerializer()
    from_location = LocationsListSerializer()
    to_location = LocationsListSerializer()
    class Meta:
        model = Trip
        fields = ["id", "leaving_time", "capacity", "is_intercity", 
                  "is_onway", "description", "from_location",
                  "to_location", "user", "transport_id", "is_active",
                  "cargo", "passanger"]

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        exclude = ("is_active", )

class CommentOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


class TripDetailSrializer2(serializers.ModelSerializer):
    transport_id = TripTransportOutSerializer()
    from_location = LocationsListSerializer()
    to_location = LocationsListSerializer()
    class Meta:
        model = Trip
        fields = ["id", "leaving_time", "capacity", "is_intercity", 
                  "is_onway", "description", "from_location",
                  "to_location", "transport_id", "is_active", 
                  "cargo", "passanger"]

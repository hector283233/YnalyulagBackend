from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from transport.models import *
from GlobalVariables import *

class TransportCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Create Transport",
        request_body=TransportCreateSerializer,
        responses={200: TransportOutSerializer}
    )
    def post(self, request):
        data = request.data
        serializer = TransportCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if Transport.objects.filter(pk=serializer.data['id']).exists():
                transport_out = Transport.objects.get(pk=serializer.data['id'])
                serializer_out = TransportOutSerializer(transport_out)
                return Response({"response":"success", "data":serializer_out.data},
                                    status=status.HTTP_200_OK)
            else:
                return Response({"response": "error", "detail": MSG_UNKNOWN_ERROR})
        else:
            return Response({"response": "error", "detail":MSG_PARAMETERS_INSUFFICIENT},
                            status=status.HTTP_400_BAD_REQUEST)

class TransportUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Update Transport",
        request_body=TransportCreateSerializer,
        responses={200: TransportOutSerializer}
    )
    def put(self, request, pk):
        data = request.data
        user = request.user
        if Transport.objects.filter(pk=pk).exists():
            transport = Transport.objects.get(pk=pk)
            if transport.user != user:
                return Response({"response":"error", "detail":MSG_NOT_BELONG_TO_USER})
            serializer = TransportCreateSerializer(transport, data=data)
            if serializer.is_valid():
                serializer.save()
                transport_out = Transport.objects.get(pk=pk)
                serializer_out = TransportOutSerializer(transport_out)
                return Response({"response":"success", "data":serializer_out.data},
                                    status=status.HTTP_200_OK)
            else:
                return Response({"response":"error",
                        "detail":MSG_PARAMETERS_INSUFFICIENT},
                        status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response":"error",
                            "detail":MSG_OBJECT_NOT_FOUND},
                            status=status.HTTP_400_BAD_REQUEST)

class TransportDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Delete Transport"
    )
    def delete(self, request, pk):
        user = request.user
        if Transport.objects.filter(pk=pk).exists():
            transport = Transport.objects.get(pk=pk)
            if transport.user != user:
                return Response({"response":"error", "detail":MSG_NOT_BELONG_TO_USER})
            transport.delete()
            return Response({"response":"success", "message": MSG_OBJECT_DELETED}, 
                                status=status.HTTP_200_OK)
        else:
            return Response({"response":"error",
                            "detail":MSG_OBJECT_NOT_FOUND},
                            status=status.HTTP_400_BAD_REQUEST)
        
class TripCreate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Create Trip",
        request_body=TripCreateSerializer,
        responses={200: TripOutSerializer}
    )
    def post(self, request):
        data = request.data
        serializer = TripCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if Trip.objects.filter(pk=serializer.data['id']).exists():
                trip_out = Trip.objects.get(pk=serializer.data['id'])
                serializer_out = TripOutSerializer(trip_out)
                return Response({"response":"success", "data":serializer_out.data},
                                    status=status.HTTP_200_OK)
            else:
                return Response({"response": "error", "detail": MSG_UNKNOWN_ERROR})
        else:
            return Response({"response": "error", "detail":MSG_PARAMETERS_INSUFFICIENT},
                            status=status.HTTP_400_BAD_REQUEST)

class TripUpdate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Update Trip",
        request_body=TripCreateSerializer,
        responses={200: TripOutSerializer}
    )
    def put(self, request, pk):
        data = request.data
        user = request.user
        if Trip.objects.filter(pk=pk).exists():
            trip = Trip.objects.get(pk=pk)
            if trip.user != user:
                return Response({"response":"error", "detail":MSG_NOT_BELONG_TO_USER})
            serializer = TripCreateSerializer(trip, data=data)
            if serializer.is_valid():
                serializer.save()
                trip_out = Trip.objects.get(pk=pk)
                serializer_out = TripOutSerializer(trip_out)
                return Response({"response":"success", "data":serializer_out.data},
                                    status=status.HTTP_200_OK)
            else:
                return Response({"response":"error",
                        "detail":MSG_PARAMETERS_INSUFFICIENT},
                        status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response":"error",
                            "detail":MSG_OBJECT_NOT_FOUND},
                            status=status.HTTP_400_BAD_REQUEST)

class TripDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Delete Trip"
    )
    def delete(self, request, pk):
        user = request.user
        if Trip.objects.filter(pk=pk).exists():
            trip = Trip.objects.get(pk=pk)
            if trip.user != user:
                return Response({"response":"error", "detail":MSG_NOT_BELONG_TO_USER})
            trip.delete()
            return Response({"response":"success", "message": MSG_OBJECT_DELETED}, 
                                status=status.HTTP_200_OK)
        else:
            return Response({"response":"error",
                            "detail":MSG_OBJECT_NOT_FOUND},
                            status=status.HTTP_400_BAD_REQUEST)
        
class TripFilter(APIView, LimitOffsetPagination):
    from_location = openapi.Parameter("from_location", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    to_location = openapi.Parameter("to_location", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    leaving_time = openapi.Parameter("leaving_time", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    is_intercity = openapi.Parameter('is_intercity', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    is_onway = openapi.Parameter('is_onway', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    description = openapi.Parameter("description", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    created = openapi.Parameter('created', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    cargo = openapi.Parameter('cargo', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    passanger = openapi.Parameter('passanger', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    @swagger_auto_schema(
        manual_parameters=[from_location, to_location, leaving_time, cargo, 
                           passanger, is_intercity, is_onway, description, 
                           created],
        operation_description='Filter Trip',
        responses={200: TripListSerializer}
    )
    def get(self, request):
        from_location = request.query_params.get("from_location", None)
        to_location = request.query_params.get("to_location", None)
        leaving_time_start = request.query_params.get("leaving_time_start", None)
        leaving_time_end = request.query_params.get("leaving_time_end", None)
        is_intercity = request.query_params.get("is_intercity", None)
        is_onway = request.query_params.get("is_onway", None)
        description = request.query_params.get("description", None)
        created = request.query_params.get("created", None)
        cargo = request.query_params.get("cargo", None)
        passanger = request.query_params.get("passanger", None)

        trips = Trip.objects.filter()

        if from_location and to_location:
            trips = trips.filter(from_location=from_location, to_location=to_location)
        
        if leaving_time_start and leaving_time_end:
            trips = trips.filter(leaving_time__range=[leaving_time_start, leaving_time_end])
        if is_intercity == "true":
            trips = trips.filter(is_intercity=True)
        if is_intercity == "false":
            trips = trips.filter(is_intercity=False)
        if is_onway == "true":
            trips = trips.filter(is_onway=True)
        if is_onway == "false":
            trips = trips.filter(is_onway=False)
        if cargo == "true":
            trips = trips.filter(cargo=True)
        if cargo == "false":
            trips = trips.filter(cargo=False)
        if passanger == "true":
            trips = trips.filter(passanger=True)
        if passanger == "false":
            trips = trips.filter(passanger=False)
        if description:
            trips = trips.filter(description__icontains=description)
        if created == "true":
            trips = trips.order_by("-created_at")
        if created == "false":
            trips = trips.order_by("created_at")
        
        data = self.paginate_queryset(trips, request, view=self)
        serializer = TripListSerializer(data, many=True)
        results = self.get_paginated_response(serializer.data)
        return Response({
            "response":"success",
            "data": results.data
        })

class TripDetail(APIView):
    @swagger_auto_schema(
        operation_description="Trip Detail",
        responses={200: TripDetailSrializer}
    )
    def get(self, request, pk):
        if Trip.objects.filter(pk=pk).exists():
            trip = Trip.objects.get(pk=pk)
            serializer = TripDetailSrializer(trip)
            return Response({
                        "response":"success",
                        "data": serializer.data
                    })
        else:
            return Response({
                "response":"error",
                "message": MSG_OBJECT_NOT_FOUND,
            }, status=status.HTTP_404_NOT_FOUND)
        
class CommentCreate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Create Comment",
        request_body=CommentCreateSerializer
    )
    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = CommentCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"response":"success", "message": "Teswiriňiz üstünlikli ugradyldy."})
        else:
            return Response({
                "response":"error",
                "message": MSG_PARAMETERS_INSUFFICIENT
            })
        
class CommentUpdate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Comment Update",
        request_body=CommentCreateSerializer
    )
    def put(self, request, pk):
        user = request.user
        data = request.data
        if Comments.objects.filter(pk=pk).exists():
            comment = Comments.objects.get(pk=pk)
            if comment.user != user:
                return Response({"response":"error", "detail":MSG_NOT_BELONG_TO_USER})
            serializer = CommentCreateSerializer(comment, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"response":"success", "message": "Teswiriňiz üstünlikli täzelendi."})
            else:
                return Response({"response":"error",
                        "detail":MSG_PARAMETERS_INSUFFICIENT},
                        status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"response":"error",
                            "detail":MSG_OBJECT_NOT_FOUND},
                            status=status.HTTP_400_BAD_REQUEST)

class CommentDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Comment Delete"
    )
    def delete(self, request, pk):
        user = request.user
        if Comments.objects.filter(pk=pk).exists():
            comment = Comments.objects.get(pk=pk)
            if comment.user != user:
                return Response({"response":"error", "detail":MSG_NOT_BELONG_TO_USER})
            comment.delete()
            return Response({"response":"success", "message": MSG_OBJECT_DELETED}, 
                                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"response":"error",
                            "detail":MSG_OBJECT_NOT_FOUND},
                            status=status.HTTP_400_BAD_REQUEST)
        
class LocationsList(APIView):
    @swagger_auto_schema(
        operation_summary="List of locations",
        responses={200: LocationsListSerializer}
    )
    def get(self, request):
        locations = Locations.objects.all()
        serializer = LocationsListSerializer(locations, many=True)
        return Response({"response":"success", "data":serializer.data})

class TripActiveToggle(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, active):
        if Trip.objects.filter(pk=pk).exists():
            current_trip = Trip.objects.get(pk=pk)
            if int(active) == 0:
                current_trip.is_active = False
            else:
                current_trip.is_active = True
            
            current_trip.save()
            return Response({"response":"success"})
        else:
            return Response({"response":"error",
                            "detail":MSG_OBJECT_NOT_FOUND},
                            status=status.HTTP_400_BAD_REQUEST) 
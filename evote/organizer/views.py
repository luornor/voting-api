from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView,RetrieveUpdateDestroyAPIView
from .models import Event
from .serializers import EventSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Contestant
from .serializers import ContestantSerializer,VoteSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .models import Contestant


class EventCreateView(CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new event",
        operation_description="Authenticated users (organizers) can create events.",
        tags=["Events"]
    )
    def perform_create(self, serializer):
        self.created_event = serializer.save(organizer=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "Event created successfully.",
            "event": response.data
        }
        return response


class EventListView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

    @swagger_auto_schema(
        operation_summary="List organizer's events",
        operation_description="List all events created by the authenticated organizer.",
        tags=["Events"]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Events retrieved successfully.",
            "events": serializer.data
        }, status=status.HTTP_200_OK)


class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Public single event view",
        operation_description="Anyone can view details of a specific event by ID.",
        tags=["Events"]
    )
    def get(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = self.get_serializer(event)
        return Response({
            "message": "Event retrieved successfully.",
            "event": serializer.data
        }, status=status.HTTP_200_OK)
    


class EventUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.organizer != self.request.user:
            raise PermissionDenied("You are not authorized to modify this event.")
        return obj

    @swagger_auto_schema(
        operation_summary="Update an event",
        operation_description="Allows the organizer to update their event.",
        tags=["Events"]
    )
    def put(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {
            "message": "Event updated successfully.",
            "event": response.data
        }
        return response

    @swagger_auto_schema(
        operation_summary="Delete an event",
        operation_description="Allows the organizer to delete their event.",
        tags=["Events"]
    )
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            "message": "Event deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class ContestantCreateView(CreateAPIView):
    serializer_class = ContestantSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Add a contestant to an event",
        operation_description="Organizer can add a contestant to their event.",
        tags=["Contestants"]
    )
    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event")
        event = Event.objects.get(id=event_id)
        if event.organizer != request.user:
            raise PermissionDenied("You are not authorized to add contestants to this event.")
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "Contestant added successfully.",
            "contestant": response.data
        }
        return response


class ContestantListView(ListAPIView):
    serializer_class = ContestantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Contestant.objects.filter(event__id=self.kwargs['event_id'])

    @swagger_auto_schema(
        operation_summary="List contestants for an event",
        operation_description="Anyone can view contestants in a specific event.",
        tags=["Contestants"]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Contestants retrieved successfully.",
            "contestants": serializer.data
        }, status=status.HTTP_200_OK)


class ContestantUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Contestant.objects.all()
    serializer_class = ContestantSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.event.organizer != self.request.user:
            raise PermissionDenied("You are not authorized to modify this contestant.")
        return obj

    @swagger_auto_schema(
        operation_summary="Update a contestant",
        operation_description="Allows the organizer to update a contestant in their event.",
        tags=["Contestants"]
    )
    def put(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {
            "message": "Contestant updated successfully.",
            "contestant": response.data
        }
        return response

    @swagger_auto_schema(
        operation_summary="Delete a contestant",
        operation_description="Allows the organizer to delete a contestant from their event.",
        tags=["Contestants"]
    )
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            "message": "Contestant deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class VoteCreateView(CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [AllowAny]

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')

    @swagger_auto_schema(
        operation_summary="Cast one or more votes for a contestant",
        operation_description="Anonymous users can vote for a contestant. Number of votes and amount calculated.",
        tags=["Votes"]
    )
    def create(self, request, *args, **kwargs):
        ip = self.get_client_ip(request)
        request.data['voter_ip'] = ip
        if 'quantity' not in request.data:
            request.data['quantity'] = 1  # default

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "message": f"{serializer.validated_data['quantity']} vote(s) cast successfully.",
            "vote": serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


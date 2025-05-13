from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .models import Event
from .serializers import EventSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Contestant
from .serializers import ContestantSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .models import Vote, Contestant
from .serializers import VoteSerializer
from django.db.models import Q

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


class VoteCreateView(CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [AllowAny]

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')

    @swagger_auto_schema(
        operation_summary="Cast a vote for a contestant",
        operation_description="Allows anonymous users to vote. One vote per IP per contestant.",
        tags=["Votes"]
    )
    def create(self, request, *args, **kwargs):
        ip = self.get_client_ip(request)
        contestant_id = request.data.get("contestant")

        if Vote.objects.filter(contestant_id=contestant_id, voter_ip=ip).exists():
            return Response({
                "message": "You have already voted for this contestant from this IP."
            }, status=status.HTTP_400_BAD_REQUEST)

        request.data['voter_ip'] = ip
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "message": "Vote cast successfully.",
            "vote": serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

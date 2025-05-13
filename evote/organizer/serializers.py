from rest_framework import serializers
from .models import Event
from .models import Contestant
from .models import Vote
from serializers import ContestantSerializer

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')  # or .id if you prefer
    contestants = ContestantSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'event_id',
            'organizer',
            'event_name',
            'logo_url',
            'start_date',
            'end_date',
            'vote_type',
            'max_votes_per_user',
            'price_per_vote',
            'contestants',
        ]


class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ['id', 'event', 'contestant_name', 'bio', 'photo_url', 'vote_count']
        read_only_fields = ['vote_count']



class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'contestant', 'timestamp']
        read_only_fields = ['timestamp']

from rest_framework import serializers
from .models import Event
from .models import Contestant
from .models import Vote

class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ['id', 'event', 'contestant_name', 'bio', 'photo_url', 'vote_count']
        read_only_fields = ['vote_count']


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



class VoteSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = ['id', 'contestant', 'quantity', 'timestamp', 'total_amount']
        read_only_fields = ['timestamp', 'total_amount']

    def get_total_amount(self, obj):
        price = obj.contestant.event.price_per_vote or 0
        return price * obj.quantity


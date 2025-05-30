from django.contrib import admin
from .models import Event, Contestant, Vote, Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'amount', 'quantity', 'status', 'provider', 'phone_number', 'paid_at')
    search_fields = ('reference', 'phone_number')
    list_filter = ('provider', 'status', 'created_at')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','event_name', 'event_id', 'organizer', 'vote_type', 'price_per_vote', 'start_date', 'end_date')
    search_fields = ('event_name', 'event_id', 'organizer__username')
    list_filter = ('vote_type', 'start_date', 'end_date')
    date_hierarchy = 'start_date'


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    list_display = ('contestant_name', 'event', 'vote_count', 'date_created')
    search_fields = ('contestant_name', 'event__event_name')
    list_filter = ('event',)
    date_hierarchy = 'date_created'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('contestant', 'quantity', 'voter_ip', 'timestamp')
    search_fields = ('contestant__contestant_name', 'voter_ip')
    list_filter = ('timestamp',)
    date_hierarchy = 'timestamp'

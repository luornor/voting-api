from django.urls import path
from .views import (EventCreateView, EventListView,EventDetailView,VoteCreateView,
                    ContestantCreateView, ContestantListView)

urlpatterns = [
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('contestants/create/', ContestantCreateView.as_view(), name='contestant-create'),
    path('contestants/<int:event_id>/', ContestantListView.as_view(), name='contestant-list'),

    path('votes/', VoteCreateView.as_view(), name='vote-create'),

]

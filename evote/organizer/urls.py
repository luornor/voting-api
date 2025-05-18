from django.urls import path
from .views import (EventCreateView, EventListView,EventDetailView,VoteCreateView,
                    ContestantCreateView, ContestantListView,EventUpdateDeleteView,
                    ContestantUpdateDeleteView)

urlpatterns = [
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
     path('events/<int:pk>/manage/', EventUpdateDeleteView.as_view(), name='event-manage'),
    path('contestants/<int:pk>/manage/', ContestantUpdateDeleteView.as_view(), name='contestant-manage'),

    path('contestants/create/', ContestantCreateView.as_view(), name='contestant-create'),
    path('contestants/<int:event_id>/', ContestantListView.as_view(), name='contestant-list'),

    path('votes/create/', VoteCreateView.as_view(), name='vote-create'),

]

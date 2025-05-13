from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vote

# This signal will be triggered after a Vote instance is saved
# It increments the vote count of the associated Contestant
@receiver(post_save, sender=Vote)
def increment_vote_count(sender, instance, created, **kwargs):
    if created:
        contestant = instance.contestant
        contestant.vote_count += 1
        contestant.save()

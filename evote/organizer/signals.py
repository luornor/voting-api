from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vote

# This signal will be triggered after a Vote instance is saved

@receiver(post_save, sender=Vote)
def increment_vote_count(sender, instance, created, **kwargs):
    if created:
        instance.contestant.vote_count += instance.quantity
        instance.contestant.save()


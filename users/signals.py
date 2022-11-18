from django.db.models.signals import post_save
from .models import User, Candidate
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_candidate(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_candidate(sender, instance, **kwargs):
    instance.profile.save()

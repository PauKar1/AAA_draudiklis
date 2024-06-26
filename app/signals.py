from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Klientai


@receiver(post_save, sender=User)
def create_klientai(sender, instance, created, **kwargs):
    if created:
        Klientai.objects.create(user=instance)
        # Klientai.objects.create(user=instance, el_pastas=instance.email)


@receiver(post_save, sender=User)
def save_klientai(sender, instance, **kwargs):
    instance.klientai.save()

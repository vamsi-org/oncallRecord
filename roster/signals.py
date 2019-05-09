from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from roster.models import Pharmacist


@receiver(post_save, sender=User)
def create_pharmacist(sender, instance, created, **kwargs):
    if created:
        Pharmacist.objects.create(user=instance)
    instance.pharmacist.save()


@receiver(post_save, sender=User)
def save_pharmacist(sender, instance, **kwargs):
    instance.pharmacist.save()

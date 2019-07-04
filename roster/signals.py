from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from roster.models import Staff


@receiver(post_save, sender=User)
def create_pharmacist(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user=instance)
    instance.staff.save()


@receiver(post_save, sender=User)
def save_pharmacist(sender, instance, **kwargs):
    instance.staff.save()

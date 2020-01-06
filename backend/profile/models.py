from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    """
    Database model to extend the User model
    """
    roles = (
        ('Pharmacist', 'Pharmacist'),
        ('Technician', 'Technician')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_sterile_trained = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=roles)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}: {self.role}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

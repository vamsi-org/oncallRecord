from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    """
    Setting up the model for a staff member
    """
    roles = (
        ("Pharmacist","Pharmacist"),
        ("Pharmacy Technician", "Pharmacy Technician")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=19, choices=roles)
    is_sterile_trained = models.BooleanField(default=False)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profile"

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}: {self.role}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
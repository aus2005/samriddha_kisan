from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
<<<<<<< HEAD
    """
    Extended profile model linked to Django's built-in User model.
    Includes role, city, and phone number fields.
    """
=======
>>>>>>> db2e6ad432884dfe7a479dffc3334da707f7322b
    ROLE_CHOICES = (
        ('farmer', 'किसान'),
        ('buyer', 'खरिदकर्ता'),
    )
<<<<<<< HEAD

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


# Signals to create or update Profile automatically when a User is created/updated
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile object whenever a new User is created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves the associated Profile object whenever a User is saved.
    """
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Fallback: create the profile if it doesn't exist
        Profile.objects.create(user=instance)
=======
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

# Signal to create or update user profile when user is saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
>>>>>>> db2e6ad432884dfe7a479dffc3334da707f7322b

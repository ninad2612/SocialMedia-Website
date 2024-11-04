# accounts/signals.py
import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Profile

# Delete old image on profile picture update
@receiver(pre_save, sender=Profile)
def delete_old_profile_picture(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = Profile.objects.get(pk=instance.pk).profile_picture
        except Profile.DoesNotExist:
            return
        new_image = instance.profile_picture
        if old_image and old_image != new_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)

# Delete image on profile deletion
@receiver(post_delete, sender=Profile)
def delete_profile_picture_on_delete(sender, instance, **kwargs):
    if instance.profile_picture and os.path.isfile(instance.profile_picture.path):
        os.remove(instance.profile_picture.path)

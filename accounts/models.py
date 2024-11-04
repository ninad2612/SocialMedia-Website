from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pictures', blank=True, null=True)  # Use the new subdirectory

    def __str__(self):
        return f"{self.user.username}'s Profile"
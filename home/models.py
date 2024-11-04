from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)  # The user who follows
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)  # The user being followed

    class Meta:
        unique_together = ('user', 'following')  # Ensure a user can't follow the same person multiple times

    def __str__(self):
        return f"{self.user.username} follows {self.following.username}"

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Field for images
    content_video = models.FileField(upload_to='post_videos/', blank=True, null=True)  # Field for videos
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s post"
    
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
class CustomUser(AbstractUser):
    """Custom user model with additional fields."""
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.username)



class Follow(models.Model):
    """Model to manage followers and following relationships."""
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
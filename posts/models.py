from django.db import models
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    media = models.FileField(upload_to="posts/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.title

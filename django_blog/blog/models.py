from django.db import models
from django.contrib.auth.models import User
#from __future__ import annotations
from typing import Any
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='image', blank=True, null=True, default='images/default.jpg')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)


    def __str__(self) -> str:
        return f"Profile({self.user.username})"

from django.db import models
from django.conf import settings   # ✅ use AUTH_USER_MODEL
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # ✅ changed here
        on_delete=models.CASCADE,
        related_name="posts"
    )
    image = models.ImageField(
        upload_to="image",
        blank=True,
        null=True,
        default="images/default.jpg"
    )

    tags = TaggableManager()  # Django Taggit for tagging functionality

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_date"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")  # ✅ Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # ✅ changed here
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()  # Django Taggit for tagging functionality

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"

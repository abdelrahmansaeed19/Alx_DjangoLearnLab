from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    post_title = serializers.ReadOnlyField(source="post.title")

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "post_title",
            "author",
            "author_username",
            "content",
            "created_at",
            "updated_at",
            "tags",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):
        # Ensure the request user is set as author
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    comments = CommentSerializer(many=True, read_only=True)  # ✅ nested comments

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "published_date",
            "author",
            "author_username",
            "image",
            "tags",
            "comments",
        ]
        read_only_fields = ["author", "published_date"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super().create(validated_data)

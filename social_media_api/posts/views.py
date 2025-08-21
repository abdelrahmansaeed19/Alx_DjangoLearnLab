from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post, Comment, Like
from rest_framework import viewsets, status, generics, permissions
from .pagination import PostPagination
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Q
from rest_framework.response import Response
from notifications.models import Notification


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only the author can edit or delete the object.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write only if the user is the author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-published_date")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = PostPagination

        # Filtering
    filterset_fields = ["author__username"]  # e.g. ?author__username=alice

    # Searching
    search_fields = ["title", "content"]  # e.g. ?search=django

    # Ordering
    ordering_fields = ["published_date", "title"]  # e.g. ?ordering=title
    ordering = ["-published_date"]  # default ordering

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as author
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        # Automatically assign logged-in user as author
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get users the current user follows
        following_users = self.request.user.following.all()

        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        # Get posts from followed users
        return Post.objects.filter(author__in=following_users).order_by("-published_date")
    
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ create notification for post author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )

        return Response({"status": "Post liked"}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You haven’t liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"status": "Post unliked"}, status=status.HTTP_200_OK)
        

class HomePageView(TemplateView):
    template_name = 'base.html'
    
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super(PostCreateView, self).form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super(PostUpdateView, self).form_valid(form)
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    fields = ['content']
    template_name = 'posts/comment_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        messages.success(self.request, "Comment added successfully.")
        return super(CommentCreateView, self).form_valid(form)
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    fields = ['content']
    template_name = 'posts/comment_form.html'
    success_url = reverse_lazy('post-list')
    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully.")
        return super(CommentUpdateView, self).form_valid(form)
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comment deleted successfully.")
        return super(CommentDeleteView, self).delete(request, *args, **kwargs)

class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'posts/comment_list.html'
    context_object_name = 'comments'
    paginate_by = 10

    def get_queryset(self):
        return Comment.objects.filter(post__id=self.kwargs['pk']).order_by('-created_at')

class CommentDetailView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'posts/comment_detail.html'
    context_object_name = 'comment'

    def get_queryset(self):
        return Comment.objects.filter(post__id=self.kwargs['pk']).order_by('-created_at')


class CommentListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post__id=self.kwargs["pk"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs["pk"])


class CommentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

def search_posts(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, "posts/search_results.html", {"results": results, "query": query})


class PostByTagListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__slug=tag_slug).distinct().order_by('-published_date')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag_slug')
        return context
    

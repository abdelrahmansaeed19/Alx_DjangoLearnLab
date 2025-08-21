from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        unread = queryset.filter(is_read=False)
        data = [
            {
                "actor": n.actor.username,
                "verb": n.verb,
                "timestamp": n.timestamp,
                "is_read": n.is_read,
            }
            for n in queryset
        ]

        # ✅ mark unread as read when fetched
        unread.update(is_read=True)

        return Response(data)

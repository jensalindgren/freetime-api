from django.db.models import Count
from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from myproject.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListCreateAPIView):
    """
    List all profiles or create a new profile by logging in.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__posts', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a profile instance if you own it.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__posts', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer


class ProfileDelete(generics.DestroyAPIView):
    """
    Delete a profile instance if you own it.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
from rest_framework import generics, authentication, permissions


from django.contrib.auth import get_user_model
from django.db.models import Q  # For the Django queryset filter not equal

from user.api.serializers import UserListSerializer, UserCreateSerializer, UserManageSerializer


class UserListView(generics.ListAPIView):
    User = get_user_model()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    # queryset = User.objects.all().filter(~Q(first_name='')).order_by('id')

    def get_queryset(self):
        return self.User.objects.filter(is_active=True).order_by('id')


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserManageView(generics.RetrieveUpdateDestroyAPIView):
    """Update or Retrieve own user"""
    serializer_class = UserManageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

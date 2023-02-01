from django.contrib.auth import get_user_model
from django.db.models import Q  # For the Django queryset filter not equal
from rest_framework import authentication, generics, permissions
from rest_framework.authtoken import views
from rest_framework.settings import api_settings
from user.api.serializers import (AuthTokenSerializer, UserCreateSerializer,
                                  UserListSerializer, UserManageSerializer)


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
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TokenCreateView(views.ObtainAuthToken):
    """Create a new token for authenticate the user"""
    serializer_class = AuthTokenSerializer
    # permission_classes = [permissions.IsAuthenticated]
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

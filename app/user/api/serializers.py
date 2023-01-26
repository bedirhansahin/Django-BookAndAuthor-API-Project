from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # exclude = ['password', 'groups', 'user_permissions']
        fields = ['id', 'first_name', 'last_name', 'email', 'last_login', 'is_active', 'is_staff', 'date_joined']

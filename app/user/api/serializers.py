from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers
from user.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # exclude = ['password', 'groups', 'user_permissions']
        fields = ['id', 'first_name', 'last_name', 'email', 'last_login', 'is_active', 'is_staff', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data['password'].pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save

        return user


class UserManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # exclude = ['password', 'groups', 'user_permissions']
        fields = ['first_name', 'last_name', 'email', 'password', 'is_active', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True},
            'min_length': 4,
            'required': True,
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True}
        }


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={
            'input_type': 'password',
        },
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate for the users"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            message = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(message, code='Authorization')

        attrs['user'] = user
        return attrs

import re

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .constants import (MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME,
                        PROFILE_ENDPOINT_NAME, USERNAME_PATTERN)

User = get_user_model()


class ValidateUsername:
    def validate_username(self, value):
        if value is None:
            raise serializers.ValidationError('This field may not be blank.')
        match = re.match(USERNAME_PATTERN, value)
        if not match:
            raise serializers.ValidationError('Username is not valid.')
        if value == PROFILE_ENDPOINT_NAME:
            raise serializers.ValidationError(
                f'Username "{PROFILE_ENDPOINT_NAME}" is forbidden.')
        return value


class UserBaseValidateSerializer(ValidateUsername,
                                 serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, attrs):
        users = User.objects.filter(email=attrs.get('email'))
        if len(users) > 0 and attrs['username'] != users[0].username:
            raise serializers.ValidationError('Email already in use.')
        users = User.objects.filter(username=attrs.get('username'))
        if len(users) > 0 and attrs['email'] != users[0].email:
            raise serializers.ValidationError('Email already in use.')
        return super().validate(attrs)


class UserBaseSerializer(UserBaseValidateSerializer):
    username = serializers.CharField(required=True,
                                     max_length=MAX_LENGTH_USERNAME)
    email = serializers.EmailField(required=True,
                                   max_length=MAX_LENGTH_EMAIL)

    class Meta(UserBaseValidateSerializer.Meta):
        pass


class UserCreateSerializer(UserBaseSerializer):

    class Meta(UserBaseSerializer.Meta):
        pass


class UserSerializer(UserBaseSerializer):

    class Meta(UserBaseSerializer.Meta):
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class UserTokenSerializers(ValidateUsername, serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True,
        max_length=MAX_LENGTH_USERNAME
    )
    confirmation_code = serializers.CharField(
        label=_("Confirmation Code"),
        style={'input_type': 'confirmation_code'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate_username(self, value):
        super().validate_username(value)
        get_object_or_404(User, username=value)
        return value

    def validate_confirmation_code(self, value):
        if value is None:
            raise serializers.ValidationError('This field may not be blank.')
        return value

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        confirmation_code = attrs['confirmation_code']
        check_token = default_token_generator.check_token(user,
                                                          confirmation_code)
        if not check_token:
            raise serializers.ValidationError('Bad request')
        return super().validate(attrs)


class UserPatchSerializers(UserBaseValidateSerializer):
    username = serializers.CharField(required=False,
                                     max_length=MAX_LENGTH_USERNAME)
    email = serializers.EmailField(required=False,
                                   max_length=MAX_LENGTH_EMAIL)

    class Meta(UserBaseValidateSerializer.Meta):
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class UserMeSerializers(UserPatchSerializers):
    class Meta(UserPatchSerializers.Meta):
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio'
        )

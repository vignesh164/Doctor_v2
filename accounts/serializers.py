from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

from rest_framework import serializers
from requests.exceptions import HTTPError
from rest_auth.serializers import UserDetailsSerializer

from django.contrib.auth.models import Group
from .models import UserDetails


class UserExtraDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('age', 'qualification', 'phone_no')


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    group_name = serializers.ChoiceField(choices=list(Group.objects.all().values_list('name', flat=True)),
                                         write_only=True, required=True)
    user_details = UserExtraDetailsSerializer(required=False)

    def __init__(self, *args, **kwargs):
        self.fields['group_name'].choices = list(Group.objects.all().values_list('name', flat=True))
        super(RegisterSerializer, self).__init__(*args, **kwargs)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate_group_name(self, group_name):
        try:
            Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            raise serializers.ValidationError(_("You have to create group before creating user"))
        return group_name

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'group_name': self.validated_data.get('group_name', ''),
            'user_details': self.validated_data.get('user_details', '')
        }

    def save(self, request):
        adapter = get_adapter()
        self.cleaned_data = self.get_cleaned_data()

        try:
            group = Group.objects.get(name=self.cleaned_data['group_name'])
        except Group.DoesNotExist:
            raise serializers.ValidationError(_("Group is not Available"))

        try:
            user_details = dict(self.cleaned_data['user_details'])
            user_details = UserDetails.objects.create(**user_details)
        except Exception as E:
            raise serializers.ValidationError(_("Problem while creating user details " + str(E)))

        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        user.groups.add(group)
        user.user_details = user_details
        user.save()
        return user


class UserSerializer(UserDetailsSerializer):
    user_details = UserExtraDetailsSerializer()
    roles = serializers.SerializerMethodField(read_only=True)

    def get_roles(self, obj):
        return list(obj.groups.all().values_list('name', flat=True))

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('user_details', 'roles')

    def update(self, instance, validated_data):
        extra_user_details = validated_data.pop('user_details', None)
        instance = super(UserSerializer, self).update(instance, validated_data)
        instance.user_details.age = extra_user_details['age']
        instance.user_details.qualification = extra_user_details['qualification']
        instance.user_details.phone_no = extra_user_details['phone_no']
        instance.save()
        return instance

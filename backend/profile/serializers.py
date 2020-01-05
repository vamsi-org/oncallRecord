from .models import Profile
from django.contrib.auth.models import User
from rest_framework import serializers, permissions

class UserSerializer(serializers.ModelSerializer):
    permission_classes =[permissions.AllowAny]
    class Meta:
        model = User
        exclude = (
            'id',
            'password'
        )

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    permission_classes = [permissions.AllowAny]

    class Meta:
        model = Profile
        fields = (
            "user",
            "role",
            "is_sterile_trained"
        )
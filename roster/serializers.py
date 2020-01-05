from rest_framework import serializers, permissions
from roster.models import OnCallPeriod, Call
'''
from profile.serializers import ProfileSerializer

class OnCallPeriodSerializer(serializers.ModelSerializer):
    permission_classes = [
        permissions.AllowAny
    ]
    pharmacist = ProfileSerializer(read_only=True)

    class Meta:
        model = OnCallPeriod
        exclude = (
            'id',
        )

class CallSerializer(serializers.ModelSerializer):
    permissions_classes = [
        permissions.AllowAny
    ]
    session = OnCallPeriodSerializer(read_only=True)
    pharmacist = ProfileSerializer(read_only=True)
    class Meta:
        model = Call
        exclude = (
            'id',
        )
'''
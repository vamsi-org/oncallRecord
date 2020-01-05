from profile.models import Profile
from profile.serializers import ProfileSerializer
from rest_framework import generics

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
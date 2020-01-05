'''from rest_framework import generics, viewsets, permissions
from roster.serializers import OnCallPeriodSerializer, CallSerializer
from roster.models import OnCallPeriod, Call

from rest_framework.response import Response

class OncallPeriodList(generics.ListAPIView):
    """
    This ListAPIView simply returns details for all periods

    To do: pagination! this may base off of the front end
    """
    serializer_class = OnCallPeriodSerializer
    queryset = OnCallPeriod.objects.all()


class CallViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for retriving both a list of an info on individual calls

    The idea is to present only the calls from the specific user at this stage (until
    making the search function)
    """
    serializer_class = CallSerializer  
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        return Call.objects.filter(session__pharmacist__user__username=user)
'''
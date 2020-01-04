from django.test import TestCase

from django.contrib.auth.models import User
from profile.models import Profile
from roster.models import OnCallPeriod
from datetime import datetime, timedelta


class OnCallPeriodTest(TestCase):
    def setUp(self):
        """
        Setting up a testing case for the Profile module, using a pharmacist.
        """               
        User.objects.create(
            username="TestUser", 
            first_name="Test", 
            last_name="User",
            email="test.user@testing.com"
        )

        Profile.objects.update(
            role="Pharmacist",
            is_sterile_trained=True
        )
        

        OnCallPeriod.objects.create(
            pharmacist=Profile.objects.get(username__username="TestUser"),
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=7),
            tdm=False
        )


    
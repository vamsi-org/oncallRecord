from django.test import TestCase
from django.urls import reverse
from .models import OnCall, Pharmacist
from datetime import datetime
from django.contrib.auth.models import User
# Create your tests here.


class HomeTests(TestCase):
    def setUp(self):
        OnCall.objects.create(pharmacist=Pharmacist.objects.get(user__username='TestUser'), start_date=datetime.today().date(), end_date=datetime(2019, 5, 1))

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

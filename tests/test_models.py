from django.test import TestCase


class StaffModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profile.objects.create()

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_get_absolute_url(self):
        print("Method: test absolute url")
        pass
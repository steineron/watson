from unittest import TestCase

from watson.models import User


class TestUser(TestCase):
    def setUp(self):
        User.objects.create(user_name='bond')

    def test_that_user_created(self):
        user = User.objects.get(user_name='bond')
        self.assertIsNotNone(user)
        self.assertEqual(user.user_name, 'bond')

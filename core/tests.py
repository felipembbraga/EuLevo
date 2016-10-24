# -*- coding:utf-8 -*-
from django.test import TestCase
from .models import CoreUser
# Create your tests here.


class SocialLoginTestCase(TestCase):
    def setUp(self):
        CoreUser.objects.create_user(email='teste@teste.com', password='123')

    def test_social_login(self):
        user = CoreUser.objects.get(email='teste@teste.com')
        self.assertEqual(user.sociallogin_set.count(), 0, 'Não igual')
        user.social_authenticate('12345', 1)
        print user.sociallogin_set.first().social_name
        self.assertEqual(user.sociallogin_set.count(), 1, 'Não igual')
        user.social_authenticate('12346', 1)
        print user.sociallogin_set.first().social_name
        self.assertEqual(user.sociallogin_set.count(), 1, 'Não igual')
        user.social_authenticate('12347', 2)
        print user.sociallogin_set.get(social_type=2).social_name
        self.assertEqual(user.sociallogin_set.count(), 2, 'Não igual')

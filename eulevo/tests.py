from django.db.models import Q
from django.test import TestCase
from eulevo.tasks import mount_message, notify_deal

# Create your tests here.
from core.models import CoreUser
from eulevo.models import Deal


class DealMessageTestCase(TestCase):
    available_apps = []
    fixtures = ['core', 'eulevo']

    def setUp(self):
        self.user1 = CoreUser.objects.get(email='felipe.mendes.braga@gmail.com')
        self.user2 = CoreUser.objects.get(email='mendesbraga007@gmail.com')

    def testSendMessage(self):
        deal = Deal.objects.filter(
            Q(package__owner=self.user2, travel__owner=self.user1)|Q(travel__owner=self.user2, package__owner=self.user1)
        ).first()
        self.assertIsNotNone(deal, "sem deal")
        print('remetente', deal.package.owner)
        print('viajante', deal.travel.owner)
        notify_deal.delay(deal.pk, self.user1.pk)
        # notify_deal.delay(deal.pk, self.user2.pk)


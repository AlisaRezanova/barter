from django.test import TestCase, Client
from unicodedata import category

from .models import Ad, ExchangeProposal
from django.contrib.auth.models import User
from django.urls import reverse
from .views import edit_ad
import json


class AdViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='User123', password='123456')
        self.client = Client()
        self.client.login(username='User123', password='123456')
        self.ad1 = Ad.objects.create(user=self.user, title='Food_for_cat',
                 description='cats', category='pet_supplies', condition='new')
        self.ad2 = Ad.objects.create(user=self.user, title='Laptop', description='quickly',
                                     category='electronic', condition='used')
        self.ad3 = Ad.objects.create(user=self.user, title='Cup',
                 description='a cap of tea', category='home_supplies', condition='used')
        self.ex_prop = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad3,
                                                       comment='test', status='waiting')

    def test_edit_ad(self):
        url = reverse('edit_ad', args=[self.ad1.id])
        response = self.client.post(url,
                                    {'title': 'Food_for_dog',
                                     'description': 'dogs',
                                     'category': 'pet_supplies',
                                     'condition': 'new'})
        self.assertEqual(response.status_code, 302)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Food_for_dog')

    def test_delete_ad(self):
        url = reverse('delete_ad', args=[self.ad1.id])
        response = self.client.post(url)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Good Job!')

    def test_add_ad(self):
        url = reverse('add_ad')
        response = self.client.post(url, {'title': 'Iphone',
                                     'description': 'test',
                                     'category': 'electronic',
                                     'condition': 'new'})
        self.assertEqual(response.status_code, 302)

    def test_search_ad(self):
        url = reverse('search_by_title_and_description')
        response = self.client.get(url, {'search': 'food'})
        data = json.loads(response.content)
        self.assertEqual([el['title'] for el in data['ads']], ['Food_for_cat'])

    def test_add_exchange_proposal(self):
        url = reverse('add_exchange_proposal')
        response = self.client.post(url, data=json.dumps({
            'ad_sender_id': self.ad1.id,
            'ad_receiver_id': self.ad2.id,
            'comment': 'test'}), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Good job!')

    def test_update_status(self):
        url = reverse('update_status', args=[self.ex_prop.id])
        response = self.client.post(url, data=json.dumps({'status': 'decline'}), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Good Job!')



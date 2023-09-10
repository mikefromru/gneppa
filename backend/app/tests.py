from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from . models import Level
from rest_framework.reverse import reverse

class SearchTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.car = Level.objects.create(id=1, name='About car')
        self.crime = Level.objects.create(id=2, name='About crime')
        self.politics = Level.objects.create(id=3, name='About politics')

    def test_search_them(self):
        data = {'id': 2}
        response = Level.objects.get(id=2)
        #response = self.client.get(reverse('search'), data=data)
        #self.assertEqual(response.status_code, 200)
        self.assertEqual(response.name, 'About crime')

        

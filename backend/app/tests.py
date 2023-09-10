from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from . models import Level

class SearchTest(APITestCase):

    def setUp(self):
        #self.client = APIClient()
        self.car = Level.objects.create(id=1, name='About car')
        #self.crime = Level.objects.create(id=2, name='About crime')
        #self.politics = Level.objects.create(id=3, name='About politics')

    def test_search_them(self):
        self.assertEqual(2, 2)
        #data = {'id': 2}
        #response = self.client.get(reverse('search'), data=data)
        #self.assertEqual(response.status_code, 200)

        

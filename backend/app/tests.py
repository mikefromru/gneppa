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

    def test_get_by_id(self):
        response = Level.objects.get(id=2)
        self.assertEqual(response.name, 'About crime')

    def test_search_them(self):
        data = {'q': 'About crime'}
        response = self.client.get('http://localhost:8000/api/app/search/', data=data)
        #response = self.client.get(reverse('search'), dat=data)
        #self.assertEqual(response.status_code, 200)
        #for x in response.data:
            #print(data['q'] == x['name'])
    
    def test_all(self):
        response = self.client.get('http://localhost:8000/api/app/all/')
        self.assertEqual(response.status_code, 200)

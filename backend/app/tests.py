from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from . models import Level
from rest_framework.reverse import reverse

class SearchTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        Level.objects.create(id=1, name='About car')
        Level.objects.create(id=2, name='About crime')
        Level.objects.create(id=3, name='About politics')
        Level.objects.create(id=4, name='travel')

    def test_get_index_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_get_by_id(self):
        response = Level.objects.get(id=2)
        self.assertEqual(response.name, 'About crime')

    def test_search_api(self):
        # /api/app/search/?search=money
        response = self.client.get('http://localhost:8000/api/app/search/?search=travel')
        self.assertEqual(response.status_code, 200)

        response_with_empty_list = self.client.get('http://localhost:8000/api/app/search/?search=kakeknfkeke')
        self.assertEqual(len(response_with_empty_list.data), 0)
    
    def test_all_url(self):
        response = self.client.get('http://localhost:8000/api/app/all/')
        self.assertEqual(response.status_code, 200)

    def test_delete_level(self):
        id_3 = Level.objects.get(id=3).delete()
        lst = Level.objects.all().count()
        self.assertEqual(lst, 3)

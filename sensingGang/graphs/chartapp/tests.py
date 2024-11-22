from django.test import TestCase, Client
from django.urls import reverse
from chartapp.forms import ProductForm


class ChartJSTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('index')


    def test_chart_exists(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, '<canvas id="myChart"')
        
    def test_server_connection(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
    def test_index_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chartapp/index.html')
        self.assertTrue('products' in response.context)
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], ProductForm)
        
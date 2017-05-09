from django.test import Client

from reefsource.core.tests import BaseTestCase


class ViewTests(BaseTestCase):

    def test_index_view(self):
        client = Client()

        response = client.get('/')
        self.assertEquals(response.status_code, 200)

        response = client.get('/randomstring')
        self.assertEquals(response.status_code, 200)

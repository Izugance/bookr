from django.test import TestCase, Client, RequestFactory

from ..views import welcome_view


class TestViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.factory = RequestFactory()

    def test_welcome_view(self) -> None:
        response = self.client.get("")
        self.assertEquals(response.status_code, 200)

    def test_welcome_view2(self) -> None:
        request = self.factory.get("")
        response = welcome_view(request)
        self.assertEquals(response.status_code, 200)

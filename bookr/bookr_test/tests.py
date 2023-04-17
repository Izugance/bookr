# Better to modularize tests for different components (views, models,
# etc). Create a new "tests" package (with __init__.py) in your app
# dir. Start each module name with "test," and make sure to delete the
# default "tests.py" file in the app dir.
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User, AnonymousUser

from .models import Publisher
from .views import greeting_view_user


# Testing database models.
# Data that are required to be persisted are stored inside a temporary
# database, which is destroyed when the test case ends.
#
# "Test" as a prefix to test case class names, etc.; similar to
# unittest.
#
# More specific classes than TestCase:
# -SimpleTestcase: Subclass of TestCase, For views mainly.
# -TransactionTestCase: Subclass of the previous. For test cases that
# involve database interactions, using the default test client.
# -LiveServerTestCase: Similar to the previous, but uses a live server
# create by Django.
class TestPublisher(TestCase):
    # Called everytime a method is about to be executed.
    def setUp(self) -> None:
        self.p = Publisher(
            name="Packt", website="www.packt.com", email="contact@packt.com"
        )

    def test_create_publisher(self) -> None:
        self.assertIsInstance(self.p, Publisher)

    def test_str_representation(self) -> None:
        self.assertEquals(str(self.p), "Packt")


# Testing a view.
class TestGreetingView(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_greeting_view(self) -> None:
        # "Client" supports get, post, put, delete, etc.
        # What's returned is a regular HttpResponse obj.
        # (Paths specified relative to rot project.)
        response = self.client.get("/testing/greeting/")
        self.assertEquals(response.status_code, 200)


# Testing a view with authentication using a "Client" that simulates
# a browser by placing requests to the URL endpoints.
class TestLoggedInGreetingView(TestCase):
    def setUp(self) -> None:
        test_user = User.objects.create_user(
            username="testuser", password="test_password"
        )
        test_user.save()
        self.client = Client()

    # Recall that the "setUp" method is called before every test starts.
    # Hence, a new test user is created before every test runs.
    def test_user_authenticated(self) -> None:
        login = self.client.login(username="testuser", password="test_password")
        response = self.client.get("/testing/greet_user/")
        self.assertEquals(response.status_code, 200)

    def test_user_greeting_not_authenticated(self) -> None:
        response = self.client.get("/testing/greet_user/")
        # 302 => redirect.
        self.assertEquals(response.status_code, 302)


# Testing views with authentication using a request factory => you test
# them by passing a request instance directly into the view.
class TestLoggedInGreetingView2(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.test_user.save()
        self.factory = RequestFactory()

    def test_user_greeting_not_authenticated(self):
        # You have the post, put, delete methods also.
        request = self.factory.get("/testing/greet_user/")
        request.user = AnonymousUser()
        response = greeting_view_user(request)
        self.assertEquals(response.status_code, 302)

    def test_user_greeting_not_authenticated(self):
        request = self.factory.get("/testing/greet_user/")
        request.user = self.test_user
        response = greeting_view_user(request)
        self.assertEquals(response.status_code, 200)

    # NOTE: To test a class-based view =>
    # response = <ClassView>.as_view()(request)

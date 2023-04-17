from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Book, Review, Publisher, Contributor

# The created instances are in a test database, which is separate from
# your normal project's database.
class TestPublisherModel(TestCase):
    def test_publisher_creation(self) -> None:
        publisher = Publisher.objects.create(
            name="Test Publisher",
            website="www.testpublisher.com",
            email="pub@test.com",
        )
        self.assertIsInstance(publisher, Publisher)


class TestContributorModel(TestCase):
    def test_contributor_creation(self) -> None:
        contributor = Contributor.objects.create(
            first_names="Test",
            last_names="Contributor",
            email="contrib@test.com",
        )
        self.assertIsInstance(contributor, Contributor)


class TestBookModel(TestCase):
    def setUp(self) -> None:
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            website="www.testpublisher.com",
            email="testpub@test.com",
        )
        # We need the "create" method here to make sure the obj has an
        # id, which is required for many-to-many relationship
        # creations.
        self.contributor = Contributor.objects.create(
            first_names="Test",
            last_names="Contributor",
            email="contrib@test.com",
        )

    def test_book_creation(self) -> None:
        book = Book.objects.create(
            title="Test book",
            publication_date=datetime.now(),
            isbn="12345",
            publisher=self.publisher,
        )
        book.contributors.add(self.contributor)
        self.assertIsInstance(book, Book)


class TestReviewModel(TestCase):
    def setUp(self) -> None:
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            website="www.testpublisher.com",
            email="pub@test.com",
        )
        self.contributor = Contributor.objects.create(
            first_names="Test",
            last_names="Contributorr",
            email="contrib@test.com",
        )
        self.book = Book.objects.create(
            title="Test",
            publication_date=datetime.now(),
            isbn="12345",
            publisher=self.publisher,
        )
        self.book.contributors.add(self.contributor)
        self.creator = User.objects.create(username="test", password="user")

    def test_review_creation(self) -> None:
        review = Review.objects.create(
            content="Test content", rating=3, creator=self.creator, book=self.book
        )
        self.assertIsInstance(review, Review)

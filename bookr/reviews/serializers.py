# You need to be able to convert model data (Python objs) to JSON for
# client (frontend) -> server (backend) info transfers.
#
# The Serializer class can also deserialize JSON objs to Python
# equivalents.
from typing import Any

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from .models import Book, BookContributor, Contributor, Review
from .utils import average_rating


class PublisherSerializer(serializers.Serializer):
    # You put the model attrs of interest and their equivalent fields
    # here. (Manual method.)
    name = serializers.CharField()
    website = serializers.URLField()
    email = serializers.EmailField()


# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     publication_date = serializers.DateField()
#     isbn = serializers.CharField()
#     # Recall the ForeignKey relationship in the model. Hence, you need
#     # a "Publisher" serializer to serialize this instance.
#     publisher = PublisherSerializer()


# Equivalent to the previous.
class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()  # A needed customization.
    # The following use "SerializerMethodField" since the methods they
    # reference are built in this class.
    rating = serializers.SerializerMethodField("book_rating")
    reviews = serializers.SerializerMethodField("book_reviews")

    def book_rating(self, book: Book) -> float | None:
        reviews = book.review_set.all()
        if reviews:
            return average_rating([review.rating for review in reviews])
        else:
            return None  # Converted to "null" in json.

    def book_reviews(self, book: Book) -> dict[str, Any] | None:
        reviews = book.review_set.all()
        if reviews:
            # Note that it's the data we're returning.
            return ReviewSerializer(reviews, many=True).data
        else:
            return None

    class Meta:
        model = Book
        # Note that we still include the above defined fields here.
        fields = ["title", "publication_date", "isbn", "publisher", "rating", "reviews"]


class ContributionSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BookContributor
        fields = ["book", "role"]


class ContributorSerializer(serializers.ModelSerializer):
    # Consider setting the "read_only" arg to "True."
    bookcontributor_set = ContributionSerializer(many=True)
    # Consider setting "num_contributions" as a "ReadOnlyField."

    class Meta:
        model = Contributor
        fields = [
            "first_names",
            "last_names",
            "email",
            "bookcontributor_set",
            "num_contributions",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class ReviewSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    # The following uses only the string representation of a Book (in
    # this case, our "__str__" method).
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "pk",
            "content",
            "date_created",
            "date_edited",
            "rating",
            "creator",
            "book",
            "book_id",  # Note single underscore.
        ]

    # Model serializers have the "create" and "update" methods.
    def create(self, validated_data: dict[str, Any]) -> Review:
        request = self.context["request"]  # Need request data.
        creator = request.user

        if not creator.is_authenticated:
            raise NotAuthenticated("Authentication required")

        book = Book.objects.get(pk=request.data["book_id"])
        return Review.objects.create(
            content=validated_data["content"],
            book=book,
            creator=creator,
            rating=validated_data["rating"],
        )

    def update(self, instance: Review, validated_data: dict[str, Any]) -> Review:
        request = self.context["request"]
        creator = request.user

        if not creator.is_authenticated or instance.creator_id != creator.pk:
            raise PermissionDenied(
                "Permission denied, you are not the creator of this review"
            )

        instance.content = validated_data["content"]
        instance.rating = validated_data["rating"]
        instance.date_edited = timezone.now()
        instance.save()
        return instance

# Better to have your API code in a separate file.
# NOTE: The REST protocol is stateless.
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

# Viewsets help combine multiple views into one class.
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

# Authentication.
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import Book, Contributor, Review
from .serializers import BookSerializer, ContributorSerializer, ReviewSerializer


@api_view()
def book_count(request: HttpRequest) -> HttpResponse:
    # Default list of allowed "http_method_names" has "GET."
    book_count = Book.objects.count()
    return Response({"book_count": book_count})


@api_view(http_method_names=["GET"])
def book_list(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    book_serializer = BookSerializer(books, many=True)
    return Response(book_serializer.data)


# Class-based views are mostly used.
class Login(APIView):
    # We make only the "post" method allowed.
    def post(self, request: HttpRequest) -> HttpResponse:
        # Return a "User" obj if the credentials are valid.
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )

        if not user:
            return Response(
                {"error": "credentials are incorrect or user does not exist"},
                status=HTTP_404_NOT_FOUND,
            )

        # NOTE new queryset method.
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)


# (Equivalent to the "book_list" view.)
class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ContributorView(ListAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer


# Model viewsets can be used for listing and instance details concerns.
# They also help create, update, and delete records.
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.order_by("-date_created")
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = []


# A read-only model viewset is similar to a model viewset, only that
# you can't create/update/delete records.
class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # The "TokenAuthentication" system requires the token being passed
    # in the header with every request to the url mapped to this view.
    # This can be done with from the command line with the "curl"
    # command
    # authentication_classes = [TokenAuthentication]  # Can add >1.
    # permission_classes = [IsAuthenticated]
    #
    # Since we're gonna allow unauthenticated users to access our data,
    # we can do this (or don't put them at all):
    authentication_classes = []
    permission_classes = []

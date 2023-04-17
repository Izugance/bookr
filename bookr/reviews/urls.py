from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views, api_views

# A router helps map viewsets to urls.
router = DefaultRouter()
# Note the usage of raw strings.
router.register(r"books", api_views.BookViewSet)
router.register(r"reviews", api_views.ReviewViewSet)

# NOTE: The "name" arg is what is used to reference the url pattern
# if, say, you're using the "url" template tag or reverse url
# matchings.
urlpatterns = [
    path("", views.index_view, name="index_view"),
    # -----Manual API paths-----
    # (Commented out because we now use a router.)
    # path("api/book_count/", api_views.book_count, name="book_count_api"),
    # path("api/book_list_func/", api_views.book_list, name="book_list_func_api"),
    # path("api/book_list/", api_views.BookListView.as_view(), name="book_list_api"),
    # path(
    #     "api/contributors/",
    #     api_views.ContributorView.as_view(),
    #     name="contributors_api",
    # ),
    #
    # -----API paths with viewsets and a router-----
    path("api/login", api_views.Login.as_view(), name="login"),
    # All paths starting with "api/" get mapped to the router's urls.
    # We can thus use "api/books" or "api/books/1" since we've
    # the books viewset that supports book listing and book details.
    path("api/", include((router.urls, "api"))),
    # -----Paths to regular views-----
    path("books/", views.book_list, name="book_list"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/<int:book_pk>/reviews/new/", views.review_edit, name="review_create"),
    path(
        "books/<int:book_pk>/reviews/<int:review_pk>/",
        views.review_edit,
        name="review_edit",
    ),
    path("books/<int:pk>/media/", views.book_media, name="book_media"),
    path("book-search/", views.book_search, name="book_search"),
    # We're using the same view for two URL mappings.
    path("publishers/<int:pk>/", views.publisher_edit, name="publisher_edit"),
    path("publishers/new/", views.publisher_edit, name="publisher_create"),
    path("react_example/", views.react_example),
]

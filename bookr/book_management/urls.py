from django.urls import path

from .views import (
    BookRecordFormView,
    FormSuccessView,
    DeleteSuccessView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    BookDetailView,
)

urlpatterns = [
    path("new_book_record/", BookRecordFormView.as_view(), name="book_record_form"),
    path("entry_success/", FormSuccessView.as_view(), name="form_success"),
    path("delete_success/", DeleteSuccessView.as_view(), name="delete_success"),
    path("book_record_create/", BookCreateView.as_view(), name="book_create"),
    path("book_record_update/<int:pk>/", BookUpdateView.as_view(), name="book_update"),
    path("book_record_delete/<int:pk>/", BookDeleteView.as_view(), name="book_delete"),
    # Avoid name clashes.
    path("book_detail/<int:pk>/", BookDetailView.as_view(), name="book_detail_2"),
]

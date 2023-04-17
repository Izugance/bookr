"""Playing with class-based views."""

from django.shortcuts import render
from django.views import View
from django.forms import Form
from django.http import HttpRequest, HttpResponse

# Can instead import from django.views.generic.
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic import DetailView


from .forms import BookForm
from .models import Book


class BookRecordFormView(FormView):
    template_name = "book_management/book_form.html"
    form_class = BookForm
    # In the urlpatterns, this is linked to FormSuccessView.
    # NOTE: If you don't put the leading slash, you get an error.
    success_url = "/bookmgt/entry_success"

    def form_valid(self, form: Form) -> HttpResponse:
        # This method should always return an HttpResponse.
        # It is called when the form's validation is successful.
        form.save()
        # Successful validation => redirect to success_url.
        return super().form_valid(form)


class FormSuccessView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return HttpResponse("Book record saved successfully")


# Repetitive. Find a way to abstract this into the above, with a way
# to pass the success message into the view.
class DeleteSuccessView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return HttpResponse("Book record deleted")


class BookCreateView(CreateView):
    model = Book
    fields = ("name", "author")
    # NOTE: "template_name," not "template."
    template_name = "book_management/book_form.html"
    success_url = "/bookmgt/entry_success"


class BookUpdateView(UpdateView):
    model = Book
    fields = ("name", "author")  # Updatable.
    template_name = "book_management/book_form.html"
    success_url = "/bookmgt/entry_success"


class BookDeleteView(DeleteView):
    model = Book
    template_name = "book_management/book_delete_form.html"
    success_url = "/bookmgt/delete_success"


class BookDetailView(DetailView):
    # The found object is passed as context into the html file as
    # "object."
    model = Book
    template_name = "book_management/book_detail.html"


# Checkout "ListView" and other cool stuff.

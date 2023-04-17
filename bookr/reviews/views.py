"""Function-based views with Django."""

from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect

# For registering a message for user that a model obj was edited/
# created:
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.core.files.images import ImageFile

# Authentication concerns:
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import (
    # permission_required,
    user_passes_test,
    login_required,
)

# The preferred way to import the project's settings is:
# "from django.conf import settings." You can then access variable
# like "settings.DEBUG."

from PIL import Image

from .models import Book, Contributor, Publisher, Review
from .utils import average_rating
from .forms import SearchForm, PublisherForm, ReviewForm, BookMediaForm


def welcome_view(request: HttpRequest) -> HttpResponse:
    name = request.GET.get("name") or "Bookr"
    # To use a default value, you could have ....get('name', '<default>
    # ').
    # You can then do something crazy like
    # 127.0.0.1:8000/?name=Izu. (Could exclude the final
    # slash, or could set name= [i.e. empty string].)
    #
    # Could also combine args as say, ?name=Izu&
    # age=21&height=6.0&height=6.1.
    #
    # Notice that we can add multiple values for the same key,
    # since the request.GET (also request.POST) attribute refers
    # to a QueryDict instance, which supports such a thing.
    #
    # If ....GET['name'] were used and name had multiple values,
    # the last would be returned. KeyError if no key 'name.'
    # ....GET.getlist('name') would return all values. Empty list
    # if no key 'name.'
    # return HttpResponse(f'Welcome to {name}!')

    # Make the 'name' variable accessible in the template.
    context = {"name": name}
    # 'request' is an HttpRequest object, while render is a shortcut
    # function that returns an HttpResponse object.
    return render(request, "base.html", context=context)


def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, "reviews/index.html")


def book_list(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    book_list = []
    for book in books:
        # Recall many-to-one relationship.
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append(
            {
                "book": book,
                "book_rating": book_rating,
                "number_of_reviews": number_of_reviews,
            }
        )
    context = {"book_list": book_list}
    return render(request, "reviews/book_list.html", context)


def book_detail(request: HttpRequest, pk: int) -> HttpResponse:
    # 'pk' could really be 'Any.'
    # For views that try to get a single object from the database,
    # it's better to use the "get_object_or_404" function.
    book = get_object_or_404(Book, pk=pk)  # Could use 'id' instead.

    # Playing with sessions. Keeping the 10 recently viewed books.
    if request.user.is_authenticated:
        max_viewed_books_length = 10
        viewed_books = request.session.get("viewed_books", [])
        viewed_book = [book.id, book.title]
        if viewed_book in viewed_books:
            # Inefficient, but works for this small-list case.
            viewed_books.pop(viewed_books.index(viewed_book))
        viewed_books.insert(0, viewed_book)
        viewed_books = viewed_books[:max_viewed_books_length]
        # NOTE: Be careful not to assign request.session itself to a
        # new dict. It has some important info already as it is.
        request.session["viewed_books"] = viewed_books

    reviews = book.review_set.all()  # Many-to-one relationship.
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
    else:
        book_rating = None

    context = {"book": book, "book_rating": book_rating, "reviews": reviews}
    return render(request, "reviews/book_detail.html", context=context)


def book_search(request: HttpRequest) -> HttpResponse:
    # You can initialize a form with GET or POST data (bounded form)
    # or nothing (unbound form).
    search_form = SearchForm(request.GET)
    search_history = request.session.get("search_history", [])

    books = set()
    # Need this conditional ordering because "cleaned_data" is only
    # accessible if "is_valid()" returns True.
    if search_form.is_valid() and (
        search_text := search_form.cleaned_data.get("search")
    ):
        search_in = search_form.cleaned_data.get("search_in", "title")
        if search_in == "title":
            # Think of the "i" in "icontains" as "ignore case."
            # Take note of the pattern matching for filtering.
            books = Book.objects.filter(title__icontains=search_text)
        else:
            first_name_contributors = Contributor.objects.filter(
                first_names__icontains=search_text
            )
            for contributor in first_name_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

            last_name_contributors = Contributor.objects.filter(
                last_names__icontains=search_text
            )
            for contributor in last_name_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

        if request.user.is_authenticated:
            search = [search_in, search_text]
            search_history.append(search)
            request.session["search_history"] = search_history
    elif search_history:
        initial = {"search_in": search_history[-1][0]}
        # "search_text" will thus be an empty string.
        search_form = SearchForm(initial=initial)

    context = {"search_text": search_text, "form": search_form, "books": books}
    return render(request, "reviews/book_search.html", context)


# Only staff users should be able to edit publishers.
# A first approach would be to use the "permission_required('edit_
# publisher')" decorator. You could instead use the "user_passes_test"
# decorator--this allows more customization.
# Also checkout "redirect_to_login" function.
def is_user_staff(user: User) -> bool:
    return user.is_staff


# @permission_required("edit_publisher")
@user_passes_test(is_user_staff)
def publisher_edit(request: HttpRequest, pk: int | None = None) -> HttpResponse:
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == "POST":
        # Passing 'instance' helps pre-populate the form's fields with
        # model data. If instance is None, it renders the fields with-
        # out values. On submission, "request.POST" takes precedence
        # over the instance data.
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            # Save the model instance to the database, since commit is
            # True. "commit=False" => attributes updated for the new
            # (or old) model, but changes aren't saved to the database.
            # Remember, the commit argument is for ModelForm instances.
            updated_publisher = form.save()
            if publisher is None:
                messages.success(
                    request, f"Publisher '{updated_publisher}' was created."
                )
            else:
                messages.success(
                    request, f"Publisher '{updated_publisher}' was updated."
                )
            # Redirecting back to this view. Redirect could take a
            # success url, or be used like this: 1st arg is name in
            # urls.py; 2nd arg is the view's arg (could have more).
            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
        context = {
            "method": request.method,
            "form": form,
            "instance": publisher,
            "model_type": "Publisher",
        }
        return render(request, "reviews/instance_form.html", context)


@login_required
def review_edit(
    request: HttpRequest, book_pk: int, review_pk: int | None = None
) -> HttpResponse:
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk is not None:
        review = get_object_or_404(Review, pk=review_pk)
        # NOTE: "request.user" is passed by the django authentication
        # middleware.
        user = request.user
        # Using De Morgan's theorem, not(user.is_staff or review.
        # creator.id == user.id) yields the following conditional
        # check: not user.is_staff and not(review.creator.id
        # == user.id).
        if not user.is_staff and (review.creator.id != user.id):
            raise PermissionDenied
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            # To let you do extra processing before writing to
            # database.
            # Recall: "form.save" returns the updated model instance,
            # if form is a subclass of ModelForm.
            updated_review = form.save(commit=False)
            updated_review.book = book

            if review is not None:
                updated_review.date_edited = timezone.now()
                messages.success(request, f"Review for {book.title} was updated.")
            else:
                messages.success(request, f"Review for {book.title} was created.")

            updated_review.save()  # Have to call this again.
            # Makes the most sense to redirect to the book's detail.
            return redirect("book_detail", book.pk)
    else:
        form = ReviewForm(instance=review)
        context = {
            "form": form,
            "instance": review,
            "model_type": "Review",
            "related_model_type": "Book",
            "related_instance": book,
        }
        return render(request, "reviews/instance_form.html", context)


@login_required
def book_media(request: HttpRequest, pk: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        # Forms that require FileFields need the "request.FILES"
        # arg to be able to access the UploadedFile instances.
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            # "commit=False" => files not saved to disk + changes not
            # saved on model instance.
            book = form.save(commit=False)

            cover = form.cleaned_data.get("cover")
            # If you want to save an UploadedFile to a model instance's
            # File-/ImageField field, you can do something like this
            # (say 'obj' is the model instance):
            # obj.file_field = UploadedFile_instance -> obj.save().
            # "obj.file_field" stores a "FieldFile" instance, not the
            # actual file.
            # If instead you want to store an existing file on disk on
            # a model instance, you take a native Python file/file-like
            # object, wrapped in Django's "File" or "ContentFile".
            # file = open(<filepath>)
            # f = File(file), or
            # f = ContentFile("String") or ContentFile(b"Bytes")
            # (from django.core.files.File and djaango.core.files.base.
            # ContentFile)
            # obj.file_field.save(name="filename", content=f, save=True)
            # "save" defaults to True. If False, file is written to
            # disk, but association isn't saved on model instance. Can
            # then save with obj.save().
            if cover is not None:
                # We're taking the same approach with ImageFiles, but
                # we're saving the image to a BytesIO (could use
                # StringIO) for efficiency.
                cover_image = Image.open(cover)
                cover_buffer = BytesIO()  # In-memory, quick access.
                cover_image.thumbnail(size=(300, 300))
                # NOTE: "cover.image.format" attribute.
                cover_image.save(fp=cover_buffer, format=cover.image.format)
                # 'cover_buffer' now has the contents of the image.
                #
                # For extra "width," "height" attrs we wrap with the following
                # (could use for further file verification logic):
                cover_file = ImageFile(cover_buffer)
                # Save the image on the model's field + write to disk.
                book.cover.save(name=cover.name, content=cover_file)

            # Whether or not the cover was added, you want to save the book.
            book.save()
            messages.success(request, f"Book '{book}' was saved.")
            return redirect("book_detail", book.pk)
    else:
        form = BookMediaForm(instance=book)

    context = {
        "form": form,
        "instance": book,
        "model_type": "Book",
        "is_file_upload": True,
    }
    return render(request, "reviews/instance_form.html", context)


def react_example(request: HttpRequest) -> HttpResponse:
    return render(request, "react_example.html", {"name": "Izu", "target": 5})

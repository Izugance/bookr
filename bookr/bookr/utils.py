"""Custom operations."""

import datetime

from django.db.models import Count

# from django.db.models.query import QuerySet
from reviews.models import Review, Book


# We assume that only books the users have reviewed are the ones
# they've read.
def get_books_read_by_month(username: str) -> dict[str, Book]:
    """Get books read each month by the user."""
    current_year = datetime.datetime.now().year
    books = (
        Review.objects.filter(
            creator__username__contains=username, date_created__year=current_year
        )
        .values("date_created__month")
        .annotate(book_count=Count("book__title"))
    )

    # You get a queryset of dicts: You get a queryset of dicts:
    # [{"date_created__month": <val>, "book_count": <val>}].
    return books


def get_read_books(username: str) -> list[str]:
    """Generate all books read by the user."""
    books = [
        review.book.title
        for review in Review.objects.filter(creator__username__icontains=username)
    ]
    return books

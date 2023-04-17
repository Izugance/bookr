# NOTE: You can't use namespacing with template tags.
# Hence, you just call "{% load <templatetag_file> %}" in a template.
# Django auto-checks each app's "templatetags" dir till a matching file
# is found.
from django.template import Library
from ..models import Review

register = Library()


@register.inclusion_tag("reviews/book_list_profile.html")
def book_list(username: str) -> dict[str, list[str]]:
    # Assume that each book reviewed has been read by the user.
    books = [
        # Remember, the creator attr is a reference to a User object.
        review.book.title
        for review in Review.objects.filter(creator__username=username)
    ]
    return {"book_list": books}

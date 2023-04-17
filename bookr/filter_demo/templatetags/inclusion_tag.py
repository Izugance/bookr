from django.template import Library

register = Library()

# Inclusion tags return templates that can be "merged" with the current
# template. These tags are used the same way regular tags are used.
# "filename" is the html template to be included.
@register.inclusion_tag(filename="filter_demo/book_list.html")
def book_list(books: dict[str, str]) -> dict[str, list[str]]:
    book_list = [book_name for book_name, _ in books.items()]
    # Return the context for the "book_list.html" template.
    return {"book_list": book_list}

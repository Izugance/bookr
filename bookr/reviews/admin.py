from django.contrib import admin

from .models import (
    Book,
    Contributor,
    Publisher,
    BookContributor,
    Review,
)


class BookAdmin(admin.ModelAdmin):
    # Customizing the admin interface for models.
    model = Book
    # We want two separate columns for books:
    # a) title b) isbn. Thus, we can sort by either column.
    #
    # 'list_display' can take attribute names from the model instance.
    # Or a function that takes an instance of the model class as an
    # an argument. Or a method (but you put in quotes due to future
    # future referencing) in this admin subclass that takes such
    # instance, besides self, as an arg. Or you can just define a
    # method on the model class and have list_display reference it
    # (in quotes).
    #
    # Note that such computed values (attrs) can't be sorted.
    list_display = ("title", "isbn")
    # Filtering books by publishers.
    list_filter = ("publisher", "publication_date")
    # To have useful hierarchies of temporal information.
    date_hierarchy = "publication_date"
    # To implement the search functionality - not so sophisticated.
    # ForeignKey and ManyToManyField searches are implemented with the
    # model name with double underscore and the field name.
    search_fields = ("title", "isbn", "publisher__name")

    # To get the publisher's name correctly for the search_fields
    # property:
    def get_publisher(self, book: Book) -> str:
        # NOTE: This method appears not to get called and might not be
        # necessary. RESEARCH!
        return book.publisher.name


class ReviewAdmin(admin.ModelAdmin):
    # Excluding displayed fields, e.g.:
    # exclude = ("date_edited",)
    # NOTE: It's more prudent to list the fields you want to be
    # displayed explicitly, as follows.
    # NOTE: Only non-editable fields can be specified. Also, the
    # order in which you list the fields is the order they're displayed.
    # fields = ("creator", "content", "rating", "book")
    # You could also group the fields by using fieldsets. You can omit
    # the title of a fieldset by setting it to None.
    fieldsets = (
        (None, {"fields": ("creator", "book")}),
        ("Review content", {"fields": ("content", "rating")}),
    )


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("last_names", "first_names")
    # Note the pattern matching here.
    search_fields = ("last_names__startswith", "first_names")
    list_filter = ("last_names",)


admin.site.register(model_or_iterable=Book, admin_class=BookAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(BookContributor)
admin.site.register(Publisher)
admin.site.register(Review, ReviewAdmin)

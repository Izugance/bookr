from django.db import models
from django.contrib import auth

# NOTE: If you want to update a database table with new fields, and
# without deleting the existing database, set the 'null' and 'blank'
# args to true for the fields.


class Publisher(models.Model):
    """A company that publishes books."""

    name = models.CharField(
        max_length=50,
        # The help_text can be displayed in forms.
        help_text="The name of the publisher.",
    )
    website = models.URLField(help_text="The publisher's website.")
    email = models.EmailField(help_text="The publisher's email address.")
    # Since books have a many-to-one relationship with this class, you
    # can get the book set as such: "<publisher>.book_set.all()."

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """A published book."""

    title = models.CharField(max_length=70, help_text="The title of the book.")
    publication_date = models.DateField(
        # verbose_name is a more descriptive name of the field.
        verbose_name="Date the book was published."
    )
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of the book.")
    # Since many books can have the same publisher, you have a many-
    # to-one relationship here. This can be established using foreign
    # keys, which map records in one table to a primary key in another.
    #
    # on_delete=models.CASCADE propagates the deletion of a Publisher
    # from the database to the books published by them.
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    # A contributor could work on many books, and a book could have
    # many contributors, hence a many-to-many relationship.
    #
    # Many books can be associated with a contributor, and vice-versa.
    # Hence there's a many-to-many relationship.
    # 'through' refers to an intermediary table used to store some
    # extra info about the relationship. (Both class names are in
    # quotes due to future references.)
    # Get all contributors for a book with "book.contributors.all()."
    contributors = models.ManyToManyField("Contributor", through="BookContributor")
    # we can try "book.contributors.add(contributor, through_defaults=
    # {'role': editor})."
    # You can instead use the create method, whereby you replace
    # the "contributor" arg with proper Contributor attrs.
    # You could also use the set method ("book.contributors.set"),
    # which takes a list of Contributor instances, and the
    # through_defaults arg.
    #
    # 'upload_to' is appended to MEDIA_ROOT.
    cover = models.ImageField(upload_to="book_covers/", null=True, blank=True)
    sample = models.FileField(upload_to="book_samples/", null=True, blank=True)
    # With reviews, you can have "book.review_set.all()."

    def __str__(self) -> str:
        return f"{self.title} ({self.isbn})"


class Contributor(models.Model):
    """A contributor to a Book, e.g. author, editor, co-author."""

    first_names = models.CharField(
        max_length=50, help_text="The contibutor's first name or names."
    )
    last_names = models.CharField(
        max_length=50, help_text="The contibutor's last name or names."
    )
    email = models.EmailField(help_text="The contact email for the contributor.")
    # You have to do something like "contributor.book_set.all()" since
    # there's no "contributors" attr here.

    def __str__(self) -> str:
        return self.initalled_name()

    def initalled_name(self):
        initials = (name[0] for name in self.first_names.split())
        return f"{self.last_names}, {''.join(initials)}"

    def num_contributions(self) -> int:
        return len(self.book_set.all())


# Implementing a many-to-many relationship with an intermediate table.
class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = ("AUTHOR", "Author")
        CO_AUTHOR = ("CO_AUTHOR", "Co-Author")
        EDITOR = ("EDITOR", "Editor")

    # Since this table stores info about books and contributors,
    # it has a many-to-one relationship with each of the Book and
    #
    # Many contributors can be mapped to a single book.
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # If we don't want a deleted contributor to delete associated
    # BookContributor objects, we set on_delete=models.PROTECT.
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name="The role this contributor has had in the book.",
        # The choices arg is useful when creating forms.
        choices=ContributionRole.choices,
        max_length=20,
    )


# For a one-to-one relationship, take the case that one person can have
# only one driver's license. E.g.
# class DriverLicence(models.Model):
#   person = models.OneToOneField(Person, on_delete=models.CASCADE)
#   license_number = models.CharField(max_length=50)


class Review(models.Model):
    # TextField can store larger chunks of text.
    content = models.TextField(help_text="The review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(
        # Auto add current datetime on creation => not modifiable.
        auto_now_add=True,
        help_text="The date and time the review was created.",
    )
    date_edited = models.DateTimeField(
        null=True,  # Can be an empty field in the database table.
        help_text="The date and time the review was last edited.",
    )
    creator = models.ForeignKey(
        # Get User model from django's authentication model.
        auth.get_user_model(),
        on_delete=models.CASCADE,
    )
    # Many reviews can be associated with one book. Hence, there's a
    # many-to-one relationship.
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, help_text="The Book that this review is for."
    )

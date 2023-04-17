from django import forms

from .models import Publisher, Review, Book

# Tuple of value and text description.
SEARCH_CHOICES = (("title", "Title"), ("contributor", "Contributor"))


class SearchForm(forms.Form):
    # Default label is the name of the attr, e.g., 'search.'
    # Override this with 'label' arg in Field instance.
    # Note that key name in request.POST or form.cleaned_data is
    # still the attr name as defined here.
    search = forms.CharField(
        min_length=3,
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Bookr search"}),
    )
    search_in = forms.ChoiceField(choices=SEARCH_CHOICES, required=False)


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = "__all__"
        # Can also use exclude = () to not hide everything, or just the
        # names of the fields of the fields to exclude in a list/tuple.
        # You could also use it with the "__all__" approach.


class ReviewForm(forms.ModelForm):
    # Overwriting a model's field. This renders fields as in the
    # model's attribute ordering.
    #
    # Adding a new field results in the new field being displayed
    # after the model's fields (from attributes).
    rating = forms.IntegerField(min_value=0, max_value=5)

    class Meta:
        model = Review
        exclude = ("date_edited", "book")


class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("cover", "sample")

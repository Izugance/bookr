from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Publisher, Review, Book

# Tuple of value and text description.
SEARCH_CHOICES = (("title", "Title"), ("contributor", "Contributor"))


class SearchForm(forms.Form):
    # Default label is the name of the attr, e.g., 'search.'
    # Override this with 'label' arg in Field instance.
    # Note that key name in request.POST or form.cleaned_data is
    # still the attr name as defined here.
    search = forms.CharField(min_length=3, required=False)
    search_in = forms.ChoiceField(choices=SEARCH_CHOICES, required=False)

    # Though we can set the "helper" attr to be a "FormHelper" instance
    # elsewhere, say a view, it's common to do it here. This instance
    # determines what attrs the form should have.
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        # Need to add a submit button. This isn't exactly a button, but
        # an input with "type=submit." "Submit(name, label)."
        self.helper.add_input(Submit("", "Search"))


class InstanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        # For a "ModelForm" instance, "self.instance" is never None,
        # even if initiated with "instance=None." (Also, "self.is_
        # bound" returns "False" even if the form is initialized with
        # data.) You can only set it explicitly to None after the
        # "super().__init__()" call, *in here.*
        # The following will not work:
        # btn_text = "Save" if self.instance is not None else "Create"
        #
        # This works:
        btn_text = "Save" if kwargs.get("instance") else "Create"
        self.helper.add_input(Submit("", btn_text))


class PublisherForm(InstanceForm):
    class Meta:
        model = Publisher
        fields = "__all__"  # NOTE: This attr must be set.
        # Can also use exclude = () to not hide everything, or just the
        # names of the fields of the fields to exclude in a list/tuple.
        # You could also use it with the "__all__" approach.


class ReviewForm(InstanceForm):
    # Overwriting a model's field. This renders fields as in the
    # model's attribute ordering.
    #
    # Adding a new field results in the new field being displayed
    # after the model's fields (from attributes).
    rating = forms.IntegerField(min_value=0, max_value=5)

    class Meta:
        model = Review
        exclude = ("date_edited", "book")


class BookMediaForm(InstanceForm):
    class Meta:
        model = Book
        fields = ("cover", "sample")

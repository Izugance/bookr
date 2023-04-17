from django.template.defaultfilters import stringfilter
from django import template


# This is a singleton used to register your custom template tags and
# filters.
register = template.Library()


# Note decorator ordering.
@register.filter
# Can use the following to ensure that args supplied are converted to
# strings before working on them, to avoid issues.
@stringfilter
def explode(names: str, delimiter: str) -> list:
    # Each filter must be provided with a value to work on, and the
    # other param is optional.
    return names.split(delimiter)

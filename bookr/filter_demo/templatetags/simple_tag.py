from typing import Any

from django.template import Library

register = Library()

# We have two kinds of tags: simple tags and inclusion tags.
@register.simple_tag
def greet_user(message: str, username: str) -> str:
    return f"{message}, {username}!!!"


# If we don't want to have to pass in the args manually, but have the
# template tag automatically have access to the context from the view,
# we can do the following.
@register.simple_tag(takes_context=True)
def contextual_greet_user(context: dict[str, Any], message: str) -> str:
    # Note arg ordering.
    username = context["username"]
    return f"{message}, {username}!!!"

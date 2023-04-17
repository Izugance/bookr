from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required


def greeting_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "Hey there, welcome to Bookr! Your one stop place to review books."
    )


@login_required
def greeting_view_user(request: HttpRequest) -> HttpResponse:
    user = request.user
    return HttpResponse(f"Welcome to Bookr! {user}")

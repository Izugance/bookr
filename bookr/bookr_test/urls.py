from django.urls import path

from . import views

urlpatterns = [
    path("greeting/", views.greeting_view, name="greeting_view"),
    path("greet_user/", views.greeting_view_user, name="greet_user"),
]

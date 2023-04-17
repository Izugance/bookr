from django.urls import path

from . import views

urlpatterns = [
    path("filter/", views.filter_demo, name="filter_demo"),
    path("simpletag/", views.simple_tag_demo, name="simple_tag"),
]

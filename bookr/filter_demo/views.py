from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def filter_demo(request: HttpRequest) -> HttpResponse:
    context = {"names": "praise,eve,josh"}
    return render(request, "filter_demo/filters_tags.html", context)


def simple_tag_demo(request: HttpRequest) -> HttpResponse:
    books = {
        "Python Object-Oriented Programming": "Dusty Phillips",
        "Head First HTML and CSS": "HFLabs",
    }
    context = {"books": books, "username": "Izugance"}
    return render(request, "filter_demo/simple_tag.html", context)

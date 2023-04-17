"""Purely for the 'Testing' chapter."""
from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=50, help_text="The name of the publisher.")
    website = models.URLField(help_text="The publisher's website.")
    email = models.EmailField(help_text="The publisher's email address.")

    def __str__(self) -> str:
        return self.name

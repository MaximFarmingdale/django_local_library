from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

import uuid

class Genre(models.Model):

    """Model for the book genre"""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre"
    )
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("genre_detail", args=[str(self.id)])
    class Meta: 
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name = 'genre_name_case_insensitive_unique',
                violation_error_message= "Genre already exists (case " \
                "insenstive match)",
            )
        ]


    

    

        
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

class Book(models.Model): 

    """Model for a book but not a specfic instance of said book"""
    title = models.CharField( max_length=200, help_text="Enter the title of the book")
    author = models.ForeignKey(
        'Author', 
        on_delete=models.RESTRICT, 
        null=True,
    )

    summary = models.TextField(
        max_length= 1000, 
        help_text="Enter a brief description of the book",
    )
    isbn = models.CharField(
        max_length=13,
        unique=True,
        help_text='Enter a 13 letter <a href = "https://www.isbn-international.org/content/what-isbn">ISBN</a>'
    )
    genre = models.ManyToManyField(
        Genre, 
        help_text="Enter a genre for this book",
    )
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])



    

    

        
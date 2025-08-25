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
    language = models.ForeignKey(
        "Language",
        on_delete=models.SET_NULL, 
        null= True,
    )
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])
    def display_genre(self):
        """Creates at String for the Genre for the admin website since Genre has a many to many relationship with Book
        and cant be displayed without this function"""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    
    """Model for a specfic instance of a book"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text= "Unique ID for this book across the whole library"
    )
    book = models.ForeignKey(
        'Book', 
        on_delete=models.RESTRICT, 
        null=True,
    )
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank = True,
        default='m',
        help_text='Book availability',
    )
    def __str__(self):
        return f'{self.id} ({self.book.title})'
    class Meta:
        ordering = ['due_back']
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(
        'Died',
        null=True,
        blank=True,
    )
    def get_absolute_url(self):
        return reverse("Author_detail", args=[str(self.id)])
    def __str__(self):
        return f'{self.first_name}, {self.last_name}'
    class Meta:
        ordering = ["last_name", "first_name"]
class Language(models.Model): 
    name = models.CharField(max_length=50, unique=True, help_text="Please enter a Language")
    def get_absolute_url(self):
        return reverse("language_detail", args=[str(self.id)])
    def __str__(self):
        return self.name
    class Meta: 
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name = 'language_name_case_insensitive_unique',
                violation_error_message="Language is invalid (case insensitive match)"
            )
        ]

    

    

        
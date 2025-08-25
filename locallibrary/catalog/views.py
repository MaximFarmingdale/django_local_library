from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request): 
    """View function for the home page"""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    #Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()

    #apparently you can leave out the all method since it is implied 
    num_authors = Author.objects.all().count()
    
    context = {
        'numbooks': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
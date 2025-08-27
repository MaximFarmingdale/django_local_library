from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

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
    return render(request, 'index.html', context=context)
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10 #test it with 1 if you need to
class BookDetailView(generic.DetailView):
    model = Book
class AuthorListView(generic.ListView):
    model = Author
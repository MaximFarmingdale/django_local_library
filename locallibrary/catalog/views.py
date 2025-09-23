from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan for the current user"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    def get_queryset(self):
        return(
            BookInstance.objects.filter(borrower =self.request.user)
            .filter(status_exact='o')
            .order_by('due_back')
        )
def index(request): 
    """View function for the home page"""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    #Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()

    #apparently you can leave out the all method since it is implied 
    num_authors = Author.objects.all().count()
    num_vists = request.session.get('num_vists', 0)
    num_vists += 1
    request.session['num_vists'] = num_vists
    context = {
        'numbooks': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_vists': num_vists,
    }
    return render(request, 'index.html', context=context)
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10 #test it with 1 if you need to
class BookDetailView(generic.DetailView):
    model = Book
class AuthorListView(generic.ListView):
    model = Author
class AuthorDetailView(generic.DetailView):
    model = Author
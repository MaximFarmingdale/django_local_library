import datetime
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm 

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from models import Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan for the current user"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    def get_queryset(self):
        return(
            BookInstance.objects.filter(borrower =self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """class-based view for listing all loaned books for librarian"""
    permission_required = 'can_mark_returned'
    model = BookInstance 
    template_name = "catalog/all_bookinstance_list_borrower.html"
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')
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

@permission_required('perms.catalog.can_mark_returned', raise_exception=True)
@login_required
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'perms.catalog/book_renew_librarian.html', context)
class AuthorCreate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.change_author'
class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'perms.catalog.update_author'
class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'perms.catalog.delete_author'
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect("author-delete", kwargs={'pk': self.object.pk})


    



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote


# Create your views here.

def main(request):
    return render(request, 'app_quotes/index.html',
                  context={"title": "Quotes to Scrape", "quotes": Quote.objects.all()})


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='app_quotes:main')
        else:
            return render(request, 'app_quotes/tag.html', {'form': form})

    return render(request, 'app_quotes/tag.html', {'form': TagForm()})


def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='app_quotes:main')
        else:
            return render(request, 'app_quotes/author.html', {'form': form})

    return render(request, 'app_quotes/author.html', {'form': AuthorForm()})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to="app_quotes:main")

        return render(request,
                      "app_quotes/quote.html",
                      context={"form": form})

    return render(request,
                  "app_quotes/quote.html",
                  context={"form": QuoteForm()})


def author_detail(request, pk):
    post = get_object_or_404(Author, pk=pk)
    context = {
        'post': post,
        'fullname': post.fullname,
        'description': post.description,
        'born_date': post.born_date,
        'born_location': post.born_location,

    }
    return render(request, 'app_quotes/about-author.html', context)

from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views.generic import ListView, DetailView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
import ast

def home(request):
    return render(request, 'journal/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
        print(form)
    return render(request, 'journal/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('home')  # Змініть 'some_homepage' на ім'я вашої домашньої сторінки
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
        # print(form)
    return render(request, 'journal/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

class ArticleList(ListView):
    model = Article
    template_name = 'journal/articles.html'
    context_object_name = 'articles'
    paginate_by = 4
    ordering = ['-created_at']

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
            ).order_by('-created_at').distinct()
        else:
            return Article.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        return context
    
class ArticleDetail(DetailView):
    model = Article
    template_name = 'journal/article.html'
    slug_url_kwarg = 'article_slug'

def create_article(request):
    if request.method == 'POST':
         form = AddArticleForm(request.POST)
         if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            # slug = form.cleaned_data['slug']
            categories = form.cleaned_data['categories']
            author = request.user

            article = Article(title=title, content=content, author=author)
            article.save()
            article.categories.set(categories)

            return render(request, 'journal/add_tags.html', {'article_slug':article.slug})
    else:
        form = AddArticleForm()
        # print(form)
    context = {
        'form':form,
    }
    return render(request, 'journal/create_article.html', context)

def add_tags(request):

    print(request.GET)

    article_slug = request.GET.get('article_slug')
    print(article_slug)
    tag_list = request.GET.get('tag_list')
    print(tag_list)

    if not tag_list:
        tag_list = []

    if isinstance(tag_list, str):
        tag_list = ast.literal_eval(tag_list)
        print(tag_list)

    print(request.POST)
    name = request.POST.get('name')
    print(name)


    if request.method == 'POST':
        form = TagForm(request.POST)
        if name not in tag_list:
            tag_list.append(name)
        print(tag_list)
        if form.is_valid():
            form.save()
            return render (request, 'journal/add_tags.html', {'form': form,'tag_list':tag_list,'article_slug':article_slug})
    else:
        form = TagForm()
        
    context = {
        'form': form,
        'tag_list':tag_list,
        'article_slug':article_slug
    }
    return render(request, 'journal/add_tags.html', context)

def creating_article(request):

    print(request.GET)

    article_slug = request.GET.get('article_slug')
    print(article_slug)
    article = Article.objects.filter(slug=article_slug)[0]
    print(article)
    print(article.content)

    tag_list = request.GET.get('tag_list')
    print(tag_list)

    if not tag_list:
        tag_list = []

    if isinstance(tag_list, str):
        tag_list = ast.literal_eval(tag_list)
        print(tag_list)

    for tag in tag_list:
        tag = tag.strip()
        tag = Tag.objects.get(name=tag)
        article.tags.add(tag)

    return redirect('article_detail', article_slug)

def edit(request):
    articles = Article.objects.all().order_by('-created_at')

    context = {
        'articles':articles,
    }

    return render(request, 'journal/edit.html', context)

def edit_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = EditArticleForm(request.POST, instance=article)
        if form.is_valid():
            article.save()
            form.save()
            print(article.tags.all())
            tags = [tag.name for tag in article.tags.all()]
            print(tags)
            return render(request, 'journal/edit_tags.html', {'article_slug':article.slug, 'tag_list':tags})
    else:
        form = EditArticleForm(instance=article)
    context = {
        'form':form,
    }
    return render(request, 'journal/edit_article.html', context)

def edit_tags(request):
    print(request.GET)

    article_slug = request.GET.get('article_slug')
    print(article_slug)
    tag_list = request.GET.get('tag_list')
    print(tag_list)

    if not tag_list:
        tag_list = []

    if isinstance(tag_list, str):
        tag_list = ast.literal_eval(tag_list)
        print(tag_list)

    print(request.POST)
    name = request.POST.get('name')
    print(name)


    if request.method == 'POST':
        form = TagForm(request.POST)
        if name not in tag_list:
            tag_list.append(name)
        print(tag_list)
        if form.is_valid():
            form.save()
            return render (request, 'journal/edit_tags.html', {'form': form,'tag_list':tag_list,'article_slug':article_slug})
    else:
        form = TagForm()
        
    context = {
        'form': form,
        'tag_list':tag_list,
        'article_slug':article_slug
    }
    return render(request, 'journal/edit_tags.html', context)

def editing_article(request):

    print(request.GET)

    article_slug = request.GET.get('article_slug')
    print(article_slug)
    article = Article.objects.filter(slug=article_slug)[0]
    print(article)
    print(article.content)

    tag_list = request.GET.get('tag_list')
    print(tag_list)

    if not tag_list:
        tag_list = []

    if isinstance(tag_list, str):
        tag_list = ast.literal_eval(tag_list)
        print(tag_list)

    article.tags.clear()
    for tag in tag_list:
        tag = Tag.objects.get(name=tag)
        article.tags.add(tag)

    return redirect('article_detail', article_slug)
    # return render(request, 'journal/editing_article.html')

def delete(request):
    articles = Article.objects.all().order_by('-created_at')

    context = {
        'articles':articles,
    }

    return render(request, 'journal/delete.html', context)

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'journal/delete_article.html'
    success_url = reverse_lazy('delete')
    pk_url_kwarg = 'article_id'
    

# def delete_article(request):
#     return render(request, 'journal/delete_article.html', )

def show_category(request, category_id):
    print(request.GET)
    articles = Article.objects.filter(categories=category_id).order_by('-created_at')
    cats = Category.objects.all()

    query = request.GET.get('q')
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at').distinct()

    paginator = Paginator(articles, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles':page_obj,
        'cats': cats,
        'page_obj':page_obj,
    }
    return render(request, 'journal/articles.html', context)

def a_delete_tag(request):

    print(request.GET)
    article_slug = request.GET.get('article_slug')
    tag_list = request.GET.get('tag_list')
    tag = request.GET.get('tag')

    tag_list = ast.literal_eval(tag_list)
    tag_list.remove(tag)

    return render(request, 'journal/add_tags.html', {'tag_list':tag_list,'article_slug':article_slug})

def e_delete_tag(request):

    print(request.GET)
    article_slug = request.GET.get('article_slug')
    tag_list = request.GET.get('tag_list')
    tag = request.GET.get('tag')

    tag_list = ast.literal_eval(tag_list)
    tag_list.remove(tag)

    return render(request, 'journal/edit_tags.html', {'tag_list':tag_list,'article_slug':article_slug})
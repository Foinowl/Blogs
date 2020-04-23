from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import PostForm, TagForm
from .utils import ObjectCreateMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from .models import Post, Tag


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class TagListView(ListView):
    model = Tag
    template_name = 'blog/tag.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'tags'
    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class TagsOfPostList(ListView):
    model = Tag
    template_name = 'blog/tags_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(slug__iexact=self.request.slug)

def tags_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    post = Post.objects.filter(tags=tag)
    paginator = Paginator(post, 3)

    page_number = request.GET.get('page',1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    context = {
        'tag':tag,
        'posts': post,
        'page_obj': page,
        'is_paginated': is_paginated,
    }
    return render(request, 'blog/tags_posts.html', context)


class PostDetailView(DetailView):
    model = Post

class TagDetailView(DetailView):
    model = Tag

class PostCreateView(LoginRequiredMixin,ObjectCreateMixin,View):
    model_form = PostForm
    template = 'blog/post_form.html'


class TagCreateView(LoginRequiredMixin,ObjectCreateMixin,View):
    model_form = TagForm
    template = 'blog/tag_form.html'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class TagUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tag
    fields = ['title', 'slug']

    def test_func(self):
        return True

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class TagDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    success_url = '/'

    def test_func(self):
        return True


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):  # новый
        query = self.request.GET.get('search', '')
        if query:
            object_list = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        else:
            object_list = Post.objects.all()
        return object_list

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
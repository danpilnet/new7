from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View

from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from datetime import datetime
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.shortcuts import render, redirect


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'post'
    ordering = ''
    paginate_by = 2
    queryset = Post.objects.filter(post_news='NE')

    def get_contex_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(post_news='NE')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context




class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    context_object_name = 'create'
    success_url = '/post/'
    permission_required = ('simpleapp.add_post',
                           'simpleapp.change_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.post_news = 'AR'
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'edit'
    success_url = '/post/'
    permission_required = ('simpleapp.change_post')


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'delete'
    success_url = '/post/'


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.now()
        return context


class ArticlesDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(post_news='AR')



def author_now(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        user.groups.add(author_group)
    return redirect('/protect/')




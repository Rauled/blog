from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from .models import Post, Tag
from .utils import *
from .forms import TagForm, PostForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.db.models import Q

def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_urls = '?page={}'.format(page.previous_page_number())
    else:
        prev_urls = ''

    if page.has_next():
        next_urls = '?page={}'.format(page.next_page_number())
    else:
        next_urls = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_urls': prev_urls,
        'next_urls': next_urls
    }


    return render(request, 'blog/index.html', context=context)

class PostDetail(ObjectDetailModel, View):
    model = Post
    template = 'blog/post_detail.html'

class PostCreate(LoginRequiredMixin, ObjectCreatelModel, View):
    form_model = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True

class PostUpdate(LoginRequiredMixin, ObjectUpdateModel, View):
    model = Post
    form_model = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True

class PostDelete(LoginRequiredMixin, ObjectDeleteModel, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True

class TagDetail(ObjectDetailModel, View):
    model = Tag
    template = 'blog/tag_detail.html'

class TagCreate(LoginRequiredMixin, ObjectCreatelModel, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True

class TagUpdate(LoginRequiredMixin, ObjectUpdateModel, View):
    model = Tag
    form_model = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True

class TagDelete(LoginRequiredMixin, ObjectDeleteModel, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags':tags})

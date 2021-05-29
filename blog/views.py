from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag

def post_list(request, tag_slug=None):
    posts = Post.published.all()

    # post tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    
    # paginator
    paginator = Paginator(posts, 10)  # 10 posts in each page
    page =request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'post_list.html', {'posts':posts, page:'pages', 'tag':tag})

def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    return render(request, 'post_detail.html', {'post':post})
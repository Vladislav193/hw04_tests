from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .utils import get_page
from django.shortcuts import render, get_object_or_404
from .models import Group, Post, User
from .forms import PostForm


def index(request):
    title = 'Последние обновления'
    page_obj = get_page(Post.objects.all(), request)
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    title = f'Записи сообщества {group.title}'
    page_obj = get_page(group.posts.all(), request)
    context = {
        'group': group,
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_count = author.posts.all().count()
    title = f'Профайл пользователя {username}'
    page_obj = get_page(author.posts.all(), request)
    context = {
        'title': title,
        'posts_count': posts_count,
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_count = post.author.posts.count()
    author_post = post.author
    title = f'Пост {post.text[:30]}'
    context = {
        'post': post,
        'post_count': post_count,
        'title': title,
        'author_post': author_post
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect("posts:profile", request.user.username)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.pk)
    return render(request, 'posts/post_create.html',
                  {'form': form, 'is_edit': is_edit, 'post': post})

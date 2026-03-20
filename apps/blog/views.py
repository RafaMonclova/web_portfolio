
# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

def blog_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        posts = Post.objects.all().order_by("-created_at")
    else:
        posts = Post.objects.filter(active=True).order_by("-created_at")
    return render(request, "blog/list.html", {"posts": posts})

def blog_detail(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        post = get_object_or_404(Post, slug=slug)
    else:
        post = get_object_or_404(Post, slug=slug, active=True)
    return render(request, "blog/detail.html", {"post": post})

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/blog/?created=1')
    else:
        form = PostForm()
    
    return render(request, "blog/create.html", {"form": form})

@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Solo el autor puede editar
    if post.author != request.user:
        return redirect('blog_detail', slug=slug)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/create.html", {"form": form, "post": post})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user:
        return redirect('blog_detail', slug=slug)

    if request.method == "POST":
        post.delete()
        return redirect('blog_list')

    return redirect('blog_detail', slug=slug)

@login_required
def post_toggle_active(request, slug):
    if not request.user.is_superuser:
        return redirect('blog_list')
        
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.active = not post.active
        post.save()
        
    return redirect('blog_list')
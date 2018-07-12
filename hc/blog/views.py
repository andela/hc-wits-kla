from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils.text import slugify
from django.contrib import messages
from dateutil import parser as date_parser
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .forms import AddPostForm, AddCategoryForm, AddCommentForm
from .models import Post, Category
from django.views.decorators.csrf import csrf_exempt


@login_required
def my_posts(request):
    author = request.user
    posts_list = Post.objects.filter(author=author).order_by("-created").all()
    paginator = Paginator(posts_list, 7)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    ctx = {"posts": posts, "page": page}
    return render(request, "blog/my_posts.html", ctx)


@login_required
def add_post(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            # save  blog  post
            slug = slugify(form.cleaned_data['title'])
            post = Post(title=form.cleaned_data["title"], slug=slug,
                        body=form.cleaned_data["body"], author=request.user,
                        status=form.cleaned_data["status"],
                        category=form.cleaned_data["category"])
            try:
                post.publish = date_parser.parse(form.cleaned_data["publish"])
                post.save()
                return redirect("hc-my-posts")
            except ValueError:
                form.add_error_msg("publish", u"Enter valid date and time")
    else:
        form = AddPostForm()
    return render(request, 'blog/add_post.html', {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(
        Post, id=post_id, author=request.user)
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            # edit  blog  post
            post.slug = slugify(form.cleaned_data['title'])
            post.title = form.cleaned_data["title"]
            post.body = form.cleaned_data["body"]
            post.author = request.user
            post.status = form.cleaned_data["status"]
            post.category = form.cleaned_data["category"]
            try:
                post.publish = date_parser.parse(form.cleaned_data["publish"])
                post.save()
                return redirect("hc-my-posts")
            except ValueError:
                form.add_error_msg("publish", u"Enter valid date and time")
    else:
        form = AddPostForm(instance=post, initial={
                           "publish": post.publish.strftime("%m-%d-%Y %H:%M")})
    return render(request, 'blog/add_post.html', {"form": form})


@csrf_exempt
@login_required
def remove_post(request, post_id):
    if request.method == "DELETE":
        post = get_object_or_404(Post, author=request.user, id=post_id)
        post.delete()
        messages.success(
            request, "Post has been deleted successfully.")
        return HttpResponse({"message": "post deleted successfully"}, 200)
    else:
        return HttpResponse({"message": "Http Method Not Allowed"}, 405)


@csrf_exempt
@login_required
def add_category(request):
    author = request.user
    if request.method == "POST":
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = author
            category.save()
            messages.success(
                request, "Category has been created successfully.")
            return HttpResponse({"message": "Category has been added successfully"}, 200)
    else:
        return HttpResponse({"message": "Http method not allowed"}, 405)


def articles_list(request):
    category = request.GET.get("category", None)
    if category:
        posts_list = Post.published.filter(
            category__title__icontains=category)
    else:
        posts_list = Post.published.all()
    paginator = Paginator(posts_list, 10)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    ctx = {"posts": posts, "page": page}
    return render(request, 'blog/posts.html', ctx)


def article_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post, slug=slug, publish__year=year, publish__month=month, publish__day=day)
    if request.method == "POST":
        form = AddCommentForm(request.POST)
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(
            request, "You have commented on this blog post")
        # empty the form
        form = AddCommentForm()
    else:
        form = AddCommentForm()
    comments = post.comments.all()
    ctx = {"post": post, "form": form, "comments": comments}
    return render(request, 'blog/post_detail.html', ctx)

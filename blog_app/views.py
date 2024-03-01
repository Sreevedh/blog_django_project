from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
# from django.urls import HttpResponse
from .forms import AuthorForm
from django.contrib.auth import authenticate, login, logout
from .models import Author, Post
from django.contrib.auth.models import AbstractUser
from .forms import AuthorForm, PostForm
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
# Create your views here.

def signin(request):
    # author = AuthorForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        u = Author.objects.get(user__username=username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return render(request, 'home.html')
            return redirect('blog:home')
        else:
            return HttpResponse('Invalid credentials')
    return render(request, 'signin.html')

def signup(request):
    form = AuthorForm()
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            Author.objects.create(user_id=form.instance.id)
            return redirect('blog:signin')
    return render(request, 'signup.html', {'form':form})

@login_required
def home(request):
    post = Post.objects.all().order_by('-pub_date')
    form = {
        "post":post
    }
    return render(request, 'home.html', form)

@login_required
def profile(request,pk):
    author = Author.objects.get(user_id=pk)
    post = Post.objects.filter(author_id=author.id)
    
    forms = {
        'author':author,
        'post':post
    }

    return render(request, 'profile.html', forms)

@login_required
def post_create(request):
    page = 'create_post'
    user_id = request.user.id
    auth_id = Author.objects.get(user_id=user_id)
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            author = auth_id.id
            Post.objects.create(title=title, content=content, author_id=author)
            return redirect('blog:profile', pk=request.user.id)
    return render(request, 'create_post.html', {'form':form, 'page':page})

@login_required
def update_profile_pic(request):
    if request.method == 'POST':
        author = Author.objects.get(user_id=request.user.id)
        user_id = author.user.id

        if request.FILES:
            existing_pro_pic = author.user.profile_picture
            existing_pro_pic.delete(save=True)
            profile_picture = request.FILES['profile_picture']
            author.user.profile_picture = profile_picture
            author.user.save()
            return redirect('blog:profile', pk=user_id)
        else:
            return HttpResponse('Please select a file')
        
    return render(request, 'update_profile_pic.html')



def post_list(request):
    pass


def post_detail(request):
    pass


@login_required
def post_delete(request,pk):
    user_id = request.user.id
    delete_post = Post.objects.get(pk=pk)
    delete_post.delete()
    return redirect('blog:profile', pk=request.user.id)


@login_required
def update_post(request,pk):
    page = 'update_post'
    post = Post.objects.get(pk=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', pk=request.user.id)
    return render(request, 'create_post.html', {'form':form, 'page':page})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    response = redirect('blog:signin')
    response.delete_cookie('csrftoken')
    return response
    # logout(request)
    # return redirect('blog:signin')
    # return HttpResponse('Logged out successfully')
    # return render(request, 'signin.html')
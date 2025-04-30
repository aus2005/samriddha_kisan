from django.shortcuts import render, redirect
from .models import Post
from .forms import CreatePost
from django.contrib.auth.decorators import login_required

# Create your views here.
# def posts_list(request):
#     return render(request, 'posts/posts_list.html')

def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts': posts})

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})
@login_required(login_url='/users/login/')
def post_new(request):
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect('posts:list')  # Redirect to the posts list after saving
    else:
        form = CreatePost()  # Create an empty form for GET requests
    return render(request, 'posts/post_new.html', {'form': form})  # Pass the form to the template
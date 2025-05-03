from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostLike, Reply
from .forms import CreatePost, CreateReply
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
# def posts_list(request):
#     return render(request, 'posts/posts_list.html')

def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts': posts})

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    replies = post.replies.all().order_by('date')  # related_name='replies'

    # Handle reply submission
    if request.method == 'POST':
        if request.user.is_authenticated:
            reply_form = CreateReply(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.author = request.user
                reply.post = post
                reply.save()
                return redirect('posts:page', slug=slug)
        else:
            return redirect('users:login')  # redirect if not authenticated
    else:
        reply_form = CreateReply()

    context = {
        'post': post,
        'replies': replies,
        'reply_form': reply_form,
    }
    return render(request, 'posts/post_page.html', context)

@login_required
def toggle_like(request, slug):
    post = Post.objects.get(slug=slug)
    liked = PostLike.objects.filter(post=post, user = request.user)

    if liked.exists():
        liked.delete()
    else:
        PostLike.objects.create(post=post, user=request.user)
    return HttpResponseRedirect(reverse('posts:page', args=[slug]))

@login_required
def like_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    if request.user in reply.likes.all():
        reply.likes.remove(request.user)
    else:
        reply.likes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', 'posts:page'))
    

@login_required(login_url='/users/login/')
def post_new(request):
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect('posts:list') 
    else:
        form = CreatePost() 
    return render(request, 'posts/post_new.html', {'form': form})  
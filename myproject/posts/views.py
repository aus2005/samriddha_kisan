from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostLike, Reply
from .forms import CreatePost, CreateReply
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Case, When, IntegerField
CATEGORY_CHOICES = [
    ('important', 'महत्वपूर्ण'),
    ('crops', 'बाली'),
    ('fertilizers', 'मलहरू '),
    ('market', 'बजार'),
    ('other', 'अन्य')
]

CATEGORY_TRANSLATIONS = dict(CATEGORY_CHOICES)

def posts_list(request):
    selection = request.GET.get('sort', 'date')  # can be 'likes', 'category', 'date', or 'category:<name>'

    posts = Post.objects.exclude(slug='').annotate(
        is_important=Case(
            When(category='important', then=1),
            default=0,
            output_field=IntegerField()
        )
    )

    sort_by = 'date'
    category_filter = None

    if selection.startswith('category:'):
        category_filter = selection.split(':', 1)[1]
    elif selection in ['likes', 'category', 'date']:
        sort_by = selection

    if category_filter:
        posts = posts.filter(category__iexact=category_filter) | posts.filter(category='important')

    if sort_by == 'likes':
        posts = posts.order_by('-is_important', '-likes', '-date')
    elif sort_by == 'category':
        posts = posts.order_by('-is_important', 'category', '-date')
    else:
        posts = posts.order_by('-is_important', '-date')

    all_categories = Post.objects.exclude(category='important').values_list('category', flat=True).distinct()

    return render(request, 'posts/posts_list.html', {
    'posts': posts,
    'all_categories': all_categories,
    'selected_sort': selection,
    'category_translations': CATEGORY_TRANSLATIONS
})



def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    replies = post.replies.all().order_by('date')  # related_name='replies'
    user_has_liked = has_user_liked_post(post, request.user)
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
        'user_has_liked': user_has_liked,
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

def has_user_liked_post(post, user):
    if not user.is_authenticated:
        return False
    return PostLike.objects.filter(post=post, user=user).exists()

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
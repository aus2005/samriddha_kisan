from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Post(models.Model):
    CATEGORY_CHOICES = [('important', 'महत्वपूर्ण'), ('crops', 'बाली'), ('fertilizers', 'मलहरू '),('market', 'बजार'), ('other', 'अन्य')]
    
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField(unique=True)  
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
           
            if not base_slug:
                base_slug = f"post-{self.pk or 'new'}"
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    likes = models.ManyToManyField(User, related_name='reply_likes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Reply by {self.author} on {self.post}"
    
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} liked {self.post}"
    
    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-post__date']

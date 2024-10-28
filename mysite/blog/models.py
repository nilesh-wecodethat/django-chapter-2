from django.db import models
from django.utils  import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

class Post(models.Model) : 
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=250, 
                            unique_for_date='publish') # it ensures that the field's value is unique for entries with the same publish date.
    author = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='blog_posts')  #related_name='blog_posts' means that from the User model, you can access all posts written by a particular user (default=post_set)
    content = models.TextField()
    tags = TaggableManager()
    publish = models.DateTimeField(default=timezone.now)  # the date at post is published
    created = models.DateTimeField(auto_now_add=True)   # the date at the instance is created
    updated = models.DateTimeField(auto_now=True)  # the at at which the instance is updated
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    def get_absolute_url(self):
       return reverse('post_details', args=[self.id])  #post_details refers to the name of a URL


    class Meta:
        ordering = ('-publish',) #  For example, if you query all post, they will automatically be ordered by the descending order
    def __str__(self):  # having doubt
        return self.title


class Comment(models.Model) : 
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            related_name= "comments")
    name = models.CharField(max_length=20)
    email = models.EmailField()
    comment = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta : 
        ordering = ('createdAt',)
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    


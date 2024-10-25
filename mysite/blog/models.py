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
    slug = models.SlugField(max_length=250,    #A SlugField for the URL slug, unique for the date it is published.
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='blog_posts')  #related_name='blog_posts' means that from the User model, you can access all posts written by a particular user (default=post_set)
    content = models.TextField()
    tags = TaggableManager()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    def get_absolute_url(self):
       return reverse('post_details', args=[self.id])


    class Meta:
        ordering = ('-publish',) #  For example, if you query all post, they will automatically be ordered by the descending order
    def __str__(self):  #The __str__() method is the default human-readable representation of the object. Django will use it in many places, such as the administration site.
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
    


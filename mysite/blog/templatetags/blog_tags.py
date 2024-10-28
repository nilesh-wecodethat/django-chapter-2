from django import template
from blog.models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()  # it's used to register your own template tags and filters

@register.simple_tag(name='post_count')  # it register the function as a simple tag, If you want to register it using a different name, you can do so by specifying a name attribute, by-default is function name
def total_posts():
    return Post.objects.count()


@register.inclusion_tag("blog/post/latest_posts.html") # inclustion_tag returns a rendered template
def show_latest_posts(count=3):
    latest_posts = Post.objects.order_by('publish')[:count] 
    return {'latest_posts' : latest_posts}
    

@register.simple_tag
def get_most_commented_posts(count=3):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))



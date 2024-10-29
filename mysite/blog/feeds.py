from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from blog.models import Post

POST_COUNT = 5
TRUN_DESCRIPTION_LENGTH = 30
class LatestPostsFeed(Feed): 
    title = 'my blog'
    link = reverse_lazy('all_post')
    description = 'New posts of my blog'


    def items(self) : 
        return Post.objects.all()[:POST_COUNT]

    def item_title(self, item) : 
        return item.title

    def item_description(self, item) : 
        return truncatewords(item.content,TRUN_DESCRIPTION_LENGTH)
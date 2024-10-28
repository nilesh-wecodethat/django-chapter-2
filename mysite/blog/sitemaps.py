from django.contrib.sitemaps import Sitemap
from blog.models import Post

class PostSitemap(Sitemap) : 
    changefreq = 'weekly' # Suggests to search engines how frequently the content changes
    priority = 0.9 # Indicates the importance of this sitemap relative to others (0.0 to 1.0)

    def items(self) : 
        return Post.objects.all()

    def lastmod(self, obj) : 
        return obj.updated


"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from blog.feeds import LatestPostsFeed

sitemaps = {
    'posts' :  PostSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.all_posts, name="all_post"),
    path('tag/', views.all_posts, name="post_list_by_tag"),
    #  path('blog/', include('blog.urls', namespace='blog'))  #When you want to include another urls.py file from a different app into your main project's urls.py, you use the include function.
    path('post/<int:id>', views.post_details, name="post_details"), #This URL pattern captures an integer (id) from the URL and passes it as an argument to the post_details view.
    path('<int:post_id>/share/', views.share_post, name='share_post'),
    path('sitemap.xml', sitemap, {'sitemaps' : sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('feed/', LatestPostsFeed(), name="post_feed"),
    path('search/', views.search_post, name="search_post")
]



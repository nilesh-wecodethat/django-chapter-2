from django.shortcuts import render , get_object_or_404, redirect
from django.contrib.auth.models import User
from blog.models import Post
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from blog.forms import SendEmailForm , CommentForm, SearchPostForm
from django.core.mail import send_mail
from django.urls import reverse
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


def create_post(request): 
    ADMIN = "admin"
    TITLE= "Post title"
    SLUG = "post-slug"
    CONTENT = "Post Content"

    user = User.objects.get(username=ADMIN) 
    post = Post(title= TITLE,  
               slug= SLUG,
               content= CONTENT,
               author=user)
    post.save()


def update_post(request) :
    SLUG = 'another-post' 
    UPDATED_TITLE = "Anther Post new title"
    post = Post.objects.get(slug = SLUG)
    post.title =   UPDATED_TITLE
    post.save()


def all_posts(request, tag_slug=None) : 
    post_list = Post.objects.all()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    POST_PER_PAGE = 3
    paginator = Paginator(post_list, POST_PER_PAGE)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                    'blog/post/lists.html',
                    {'page': page,
                     'posts': posts,
                     'tag': tag})


def filter_posts(request) : 
    filtered_posts = Post.objects.filter(author__username='admin').exclude(status='draft').order_by('-publish') #The query retrieves all posts by the user 'admin', excluding drafts posts, and orders them in descending order.


def delete_post(request) : 
    post = Post.objects.get(id=1)
    post.delete()


def post_details(request, id) : 
    post = get_object_or_404(Post, id)

    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST' : 
        # new comment post
        comment_form = CommentForm(data= request.POST)
        if comment_form.is_valid() : 
            new_comment = comment_form.save(commit=False) 
            new_comment.post = post  
            new_comment.save()

            return redirect(reverse('post_details', args=[post.id])) 
    else : 
        comment_form = CommentForm()

  
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4] 

    return render(request,
                'blog\post\details.html',
                {'post_details' : post,
                'comments': comments,
                'new_comment': new_comment,
                'comment_form' : comment_form,
                'similar_posts': similar_posts})




def share_post(request, post_id) : 
    post = get_object_or_404(Post, id=post_id)
    sent = False
    HOST_EMAIL = 'patidarnilesh8120@gmail.com'
    if request.method == 'POST' : 
        form = SendEmailForm(request.POST)

        if form.is_valid() : 
            data = form.cleaned_data 
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{data['name']}\'s comments: {data['comments']}"
            send_mail(subject, message, HOST_EMAIL, [data['to']])
            sent = True

    else:  
        form = SendEmailForm()
    
    return render(request, 
                 'blog\post\share.html',
                 {'form' : form,
                 'sent': sent,
                 'post' : post})



def search_post(request) : 
    form = SearchPostForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchPostForm(request.GET)

        if form.is_valid() :
            query = form.cleaned_data['query']

            results = Post.objects.annotate(
                similarity = TrigramSimilarity('title', query) 
            ).filter(similarity__gt=0.1).order_by('-similarity')
    
    return render(request,
                'blog/post/search.html',
                {'form' : form,
                'query' : query,
                'results': results})
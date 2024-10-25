from django.shortcuts import render , get_object_or_404, redirect
from django.contrib.auth.models import User
from blog.models import Post
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from blog.forms import SendEmailForm , CommentForm
from django.core.mail import send_mail
from django.urls import reverse
from taggit.models import Tag
from django.db.models import Count



def create_post(request): 
    user = User.objects.get(username="admin") #The get() method allows you to retrieve a single object from the database.
    post = Post(title='Another post',   # create post object
               slug='another-post',
               content='Post body.',
               author=user)
    post.save()

def update_post(request) : 
    post = Post.objects.get(slug = 'another-post')
    post.title = "Anther Post new title"  #update the post field
    post.save()


def all_posts(request, tag_slug=None) : 
    post_list = Post.objects.all()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                    'blog/post/lists.html',
                    {'page': page,
                     'posts': posts,
                     'tag': tag})


def filter_posts(request) : 
    # posts =  Post.objects.filter(publish__year=2020)  #The filter() method in Django is used to retrieve records from the database that match certain criteria.
    # Post.objects.filter(publish__year=2020, author__username='admin')  #multiple filter conditions
    filtered_posts = Post.objects.filter(author__username='admin').exclude(status='draft').order_by('-publish') #The query retrieves all posts by the user 'admin', excluding drafts posts, and orders them in descending order.


def delete_post(request) : 
    post = Post.objects.get(id=1)
    post.delete()


def post_details(request, id=2) : 
    post = get_object_or_404(Post, id=2)

    # list all the active comments
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST' : 
        # new comment post
        comment_form = CommentForm(data= request.POST)
        if comment_form.is_valid() : 
            new_comment = comment_form.save(commit=False) #Create Comment object but don't save to database yet
            new_comment.post = post  #assign current Post
            new_comment.save()

            # return redirect('post', post_id=post_id)
            return redirect(reverse('post_details')) # redirecting to the /post so that in order to reload again, it does'nt create a new comment, where  "post_details" is the name we passed in to the urls.py
    else : 
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]  # having doubt


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

    if request.method == 'POST' : 
        #form submitted
        form = SendEmailForm(request.POST)

        if form.is_valid() : 
            # validation successful
            data = form.cleaned_data  # If the form is valid, you retrieve the validated data
            post_url = "post_url"
            subject = f"{data['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{data['name']}\'s comments: {data['comments']}"
            send_mail(subject, message, 'patidarnilesh8120@gmail.com',
            [data['to']])
            sent = True

    else:  # intial empty form
        form = SendEmailForm()
    
    return render(request, 
                 'blog\post\share.html',
                 {'form' : form,
                 'sent': sent,
                 'post' : post})



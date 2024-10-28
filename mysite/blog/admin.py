from django.contrib import admin
from .models import Post
from .models import Comment

# admin.site.register(Post)  #so that Post model can be managed using the Admin panel
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')   # Adds filters in the admin sidebar for the specified fields.
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish' # it adds a date-based navigation interface
    ordering = ('status', 'publish') # it sorting by status first and then by publish date. so that records with the same status are further sorted chronologically by when they were published.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'createdAt', 'active')
    list_filter = ('active', 'createdAt', 'updatedAt')
    search_fields = ('name', 'email', 'body')
from django import forms
from .models import Comment

class SendEmailForm(forms.Form) :  #Form: Allows you to build standard forms
    name = forms.CharField(max_length=25)
    to = forms.EmailField()
    email = forms.EmailField()
    comments = forms.CharField(max_length=50, required=False, widget = forms.Textarea)


class CommentForm(forms.ModelForm) :  # you can use ModelForm, which automatically generates fields corresponding to model fields.
    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment')


class SearchPostForm(forms.Form):
    query = forms.CharField()
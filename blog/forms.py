from django import forms
from .models import Profile, Post, Comment

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar')

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        fields = ('content', 'image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)
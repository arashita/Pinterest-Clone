from django import forms
from .models import Post
from boards.models import Board

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'media', 'board']  # Ensure board selection exists

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve logged-in user
        super(PostForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['board'].queryset = Board.objects.filter(user=user)  # Restrict to user's boards

from django import forms
from .models import Board

class BoardForm(forms.ModelForm):
    """Form for creating and updating boards."""
    class Meta:
        model = Board
        fields = ['name', 'description']

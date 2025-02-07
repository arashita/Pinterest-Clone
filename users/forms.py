from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)  # Optional profile picture
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture', 'bio']

class UserLoginForm(AuthenticationForm):
    """Form for user login."""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserUpdateForm(forms.ModelForm):
    """Form for updating user profile."""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture']
    profile_picture = forms.ImageField(required=False)  # Allow optional upload
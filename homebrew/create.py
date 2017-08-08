from django import forms 
from .models import Brew
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
	class Meta:
		model = Brew
		fields = ['title', 'number', 'date', 'email', 'image', 'draft', 'publish']

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']

        widgets={
        'password': forms.PasswordInput(),
        }

class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
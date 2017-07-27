from django import forms 
from .models import Brew

class PostForm(forms.ModelForm):
	class Meta:
		model = Brew
		fields = ['title', 'number', 'date', 'email', 'image']
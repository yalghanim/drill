from django.shortcuts import render
from django.http import HttpResponse
from .models import Brew
from django.shortcuts import get_object_or_404

def home(request):
	return HttpResponse("<h1>Hello World</h1>")
def fourth(request):
	return render(request, 'fourth.html', {})
def day(request):
	return HttpResponse("<h1>Day</h1>")
def task(request):
	return HttpResponse("<h1>Task</h1>") 
def allobj(request):
	post_list = Brew.objects.all()
	context = {
	"post_list": post_list,
	}
	return render(request, 'allobj.html', context) 

def intlink(request, post_number):
	obj = get_object_or_404(Brew, id = post_number)
	context = {
	"input": obj
	}
	return render(request, 'oneobj.html', context) 


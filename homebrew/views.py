from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Brew
from django.shortcuts import get_object_or_404
from .create import PostForm
from django.contrib import messages 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
	return HttpResponse("<h1>Hello World</h1>")
def fourth(request):
	return render(request, 'fourth.html', {})
def day(request):
	return HttpResponse("<h1>Day</h1>")
def task(request):
	return HttpResponse("<h1>Task</h1>") 

def allobj(request):
	post_list = Brew.objects.all() #.order_by("-date","-title") #ordering by list & title
	
	paginator = Paginator(post_list, 4)
	page = request.GET.get("page")
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	context = {
	"post_list": posts,
	}
	return render(request, 'allobj.html', context) 

def intlink(request, post_number):
	obj = get_object_or_404(Brew, id = post_number)
	context = {
	"input": obj,
	}
	return render(request, 'oneobj.html', context) 

def create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request, "Welcome to the world, Instance.")
		return redirect("homebrew:allobj")
	context = {
	"title": "Create",
	"form": form,
	}
	return render(request, 'create.html', context)

def update(request, post_number):
	instance = get_object_or_404(Brew, id=post_number)
	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		form.save()
		messages.success(request, "Ta3deel!")
		return redirect(instance.absurl())
	context = {
	"form": form,
	"instance": instance,
	"title": "Update",
	}
	return render(request, 'update.html', context)

def delete(request, post_number):
    instance = get_object_or_404(Post, id=post_number)
    instance.delete()
    messages.success(request, "Bye!")
    return redirect("homebrew:allobj")



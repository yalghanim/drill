from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Brew, Like
from django.shortcuts import get_object_or_404
from .create import PostForm, UserSignup, UserLogin
from django.contrib import messages 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout 

def userlogout(request):
    logout(request)
    return redirect("homebrew:all")

def userlogin(request):
    context = {}
    form = UserLogin()
    context['form'] = form
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('homebrew:list')

            messages.error(request, "Wrong username/password combination. Please try again.")
            return redirect("homebrew:login")
        messages.error(request, form.errors)
        return redirect("homebrew:login")
    return render(request, 'login.html', context)

def usersignup(request):
    context = {}
    form = UserSignup()
    context['form'] = form
    if request.method == 'POST':
        form = UserSignup(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            password = user.password

            user.set_password(password)
            user.save()

            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)

            return redirect("homebrew:all")
        messages.error(request, form.errors)
        return redirect("homebrew:signup")
    return render(request, 'signup.html', context)


def home(request):
	return HttpResponse("<h1>Hello World</h1>")
def fourth(request):
	return render(request, 'fourth.html', {})
def day(request):
	return HttpResponse("<h1>Day</h1>")
def task(request):
	return HttpResponse("<h1>Task</h1>") 

def allobj(request): #post_list
	today = timezone.now().date()
	# post_list = Brew.objects.all() #.order_by("-date","-title") #ordering by list & title
	post_list = Brew.objects.filter(draft=False).filter(publish__lte=today)

	query = request.GET.get("q")
	if query:
		post_list = post_list.filter(
			Q(title__icontains=query)|
			Q(number__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct()

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
	"user": request.user,
	"today": today,
	}
	return render(request, 'allobj.html', context) 

def intlink(request, post_slug): #post_detail
	obj = get_object_or_404(Brew, slug = post_slug)
	if obj.publish > timezone.now().date() or obj.draft:
		if not (request.user.is_staff or request.user.is_superuser):
			raise Http404
			
	if request.user.is_authenticated():
		if Like.objects.filter(post=obj, user=request.user).exists():
			liked = True
		else:
			liked = False
	post_like_count = obj.like_set.all().count()

	context = {
	"input": obj,
	"share_string": quote(obj.title),
	"post_like_count":post_like_count,
	"liked":liked
	}
	return render(request, 'oneobj.html', context) 

def create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		post = form.save(commit=False)
		post.author = request.user
		post.save()
		messages.success(request, "Welcome to the world, Instance.")
		return redirect("homebrew:allobj")
	context = {
	"title": "Create",
	"form": form,
	}
	return render(request, 'create.html', context)

def update(request, post_slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	instance = get_object_or_404(Brew, slug =post_slug)
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

def delete(request, post_slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	instance = get_object_or_404(Post, slug = post_slug)
	instance.delete()
	messages.success(request, "Bye!")
	return redirect("homebrew:allobj")

def ajax_like(request, post_id):
    post_object = Post.objects.get(id=post_id)
    new_like, created = Like.objects.get_or_create(user=request.user, post=post_object)

    if created:
        action="like"
    else:
        new_like.delete()
        action="unlike"

    post_like_count = post_object.like_set.all().count()
    response = {
        "action": action,
        "post_like_count": post_like_count,
    }
    return JsonResponse(response, safe=False)



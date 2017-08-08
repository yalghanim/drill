from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

class Brew(models.Model):
	title = models.CharField(max_length=50)
	author = models.ForeignKey(User, default=1)
	slug = models.SlugField(unique=True)
	number = models.IntegerField()
	date = models.DateField()
	email = models.EmailField()
	image = models.ImageField(null=True, blank=True, upload_to="post_images")
	publish = models.DateField(auto_now=False, auto_now_add=False)
	draft = models.BooleanField(default=False)


	def __str__(self):
		return self.title

	def absurl(self):
		return reverse("homebrew:intlink", kwargs={"post_slug": self.slug})

def create_slug(instance, new_slug=None):
	slug = slugify (instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Brew.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s"%(slug,qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance)

pre_save.connect(pre_save_post_reciever,sender=Brew)

class Like(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Brew)
	created = models.DateTimeField(auto_now_add=True)
	
# Create your models here.

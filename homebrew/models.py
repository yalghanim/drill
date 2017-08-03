from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save

class Brew(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(unique=True)
	number = models.IntegerField()
	date = models.DateField()
	email = models.EmailField()
	image = models.ImageField(null=True, blank=True, upload_to="post_images")

	def __str__(self):
		return self.title

	def absurl(self):
		return reverse("homebrew:intlink", kwargs={"post_number": self.id})

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

# Create your models here.

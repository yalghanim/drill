from django.db import models
from django.core.urlresolvers import reverse

class Brew(models.Model):
	title = models.CharField(max_length=50)
	number = models.IntegerField()
	date = models.DateField()
	email = models.EmailField()
	image = models.ImageField(null=True, blank=True, upload_to="post_images")

	def __str__(self):
		return self.title

	def absurl(self):
		return reverse("homebrew:intlink", kwargs={"post_number": self.id})


# Create your models here.

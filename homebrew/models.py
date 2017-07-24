from django.db import models

class Brew(models.Model):
	title = models.CharField(max_length=50)
	number = models.IntegerField()
	date = models.DateField()
	email = models.EmailField()

	def __str__(self):
		return self.title


# Create your models here.

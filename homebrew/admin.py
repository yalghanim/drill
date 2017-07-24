from django.contrib import admin
from homebrew.models import Brew

class BrewModelAdmin(admin.ModelAdmin):
	list_display = ["title", "number", "date", "email"]
	list_filter = ["title"]
	class Meta: #used to define associations
		model = Brew

admin.site.register(Brew, BrewModelAdmin)
# Register your models here.

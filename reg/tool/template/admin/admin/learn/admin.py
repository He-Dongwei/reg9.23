from django.contrib import admin
from .models import Person
from .models import School
# Register your models here.
admin.site.register(Person)
class Schooladmin(admin.ModelAdmin):
	list_display=('name','address')
	fieldsets=[
		(None,{'fields':['name']}),
		('add information',{'fields':['address','name']})
	]
admin.site.register(School,Schooladmin)
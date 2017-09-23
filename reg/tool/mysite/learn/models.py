from django.db import models

# Create your models here.


class School(models.Model):
	name=models.CharField(max_length=30)
	address=models.CharField(max_length=50)
	def __str__(self):
		return self.name
		
class Person(models.Model):
	school=models.ForeignKey(School)
	name = models.CharField(max_length=30)
	age = models.IntegerField()
	def __str__(self):
		return self.name
from django.shortcuts import render
from django.http import HttpResponse
from .models import School
# Create your views here.
def detail(request,question_id):
	return HttpResponse("You are looking at school %s." % question_id)
def results(request,question_id):
    return HttpResponse("You're looking at the results of school %s." % question_id)
def vote(request, question_id):
    return HttpResponse("You're voting on school %s." % question_id)
def index(request):
	schoolist=School.objects.all()
	return render(request, 'index.html',{'schoolist':schoolist})
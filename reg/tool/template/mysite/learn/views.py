from django.shortcuts import render

# Create your views here.
def hello(request):
	dit={}
	dit['hello']="hello world"
	return render(request,'app/index.html',dit)
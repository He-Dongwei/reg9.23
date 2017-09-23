from django.shortcuts import render
from users.models import accessrecord
# Create your views here.
def index(request):
	#Internetrecord.objects.create(user=request.user,page=request.get_full_path(),IP=request.META['REMOTE_ADDR'])
	return render(request,'index.html')

def page404(request):
	return render(request,'404.html')
from django.shortcuts import render

# Create your views here.
def search_post(request):
	ctx={}
	if request.POST:
		ctx['rlt']=request.POST['q']
	return render(request, 'home.html',ctx)
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from ..serializers import LevelSerializer
from django.core.exceptions import ObjectDoesNotExist
import os
from django.conf import settings
from django.http import FileResponse, Http404
from ..models import (
	Level,
	AppFile,
	Question,
	ClickCounter
)
from django.db.models import F
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

@method_decorator(staff_member_required, name='dispatch')
class LevelListView(ListView):

	model = Level
	paginate_by = 50
	ordering = ['created']
	template_name = 'root/level_list.html'

@staff_member_required
def detail(request, id):
	q = Question.objects.filter(level=id).values()
	bar = [x for x in q if x.get('approved')]

	return render(request, 'root/detail.html', {'q': bar})

@staff_member_required
def get_file(request, id):

	if request.method == 'POST':
		bar = Question.objects.get(id=id)
		bar.robot_voice = request.FILES['filename']
		bar.save()
		return redirect(request.META['HTTP_REFERER'])
	else:
		return HttpResponse('something went wrong')

@staff_member_required
def search(request):
	try:
		q = request.GET['q']
		name = Level.objects.filter(name__contains=q)
		return render(request, 'root/search_result.html', {'name': name})
	except KeyError:
		return render('root/search_result.html')

def index(request):
	levels = Level.objects.all()[:10]
	print(levels)
	return render(request, 'app/landing_page.html', {'levels': levels})

def download_app(request, name):
	if name == 'android':
		mob_app = 'android'
	else:
		mob_app = 'iphone'
	name = AppFile.objects.filter(platform=mob_app).first()
	filename = os.path.join(settings.MEDIA_ROOT, str(name.file))
	if os.path.exists(filename):
		response = FileResponse(open(filename, 'rb'))
		name.count += 1
		name.save()
		return response
	else:
		raise Http404

	return redirect('/')

def get_click(request, name):
	try:
		queryset = ClickCounter.objects.get(button=name)
		queryset.counter += 1
		queryset.save()
		if name == 'android':
			return redirect("https://play.google.com/store/apps/details?id=org.gneppa.gneppa&hl=en&gl=US")
		elif name == 'appgallery':
			return redirect("https://appgallery.huawei.com/app/C106945401")
	except:
		return redirect('/')

def politica(request):
	return render(request, 'app/politica.html')
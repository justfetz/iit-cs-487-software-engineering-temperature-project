
from django.shortcuts import render, get_object_or_404, redirect
#from django.utils import timezone
from temp_sensor.models import tempSensor

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView,DetailView, CreateView, UpdateView, DeleteView)
from django.utils import timezone


from django.db.models import Avg
from .forms import TempForm, SearchForm, BoundForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime


from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def forms(request):
	form = BoundForm(request.POST or None)
	if form.is_valid():
		form.save()
	else:
		form = BoundForm()
	return render(request, 'temp/forms.html', {'form': form})


class HomePageView(TemplateView):
	template_name = 'temp/index.html'
	#context_object_name = 'index'
	

class AboutView(TemplateView):
	template_name = 'temp/about.html'


class DetailListView(ListView):
	model = tempSensor

	def get_queryset(self):
		#less than or equal = lte
		#Field Lookups db queries
		return tempSensor.objects.filter(timeChanged__lte=timezone.now()).order_by('-timeChanged')

def get_list(request):
	temp_list = tempSensor.objects.order_by('timeChanged')
	date_dict = {'access_records': temp_list}
	#my_dict = {'insert_me': "Now I am from views.py"}
	return render(request, 'temp/list.html', context=date_dict)

def get_data(request, *args, **kwargs):
	data = {
		"upper": 100,
		"lower": 10,
		"average": 65,
	}
	return JsonResponse(data)

class ChartData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		qs_count = tempSensor.objects.all().count()
		currentUpperBound =  tempSensor.objects.values('upperBound').order_by('-id')[:1]
		currentLowerBound = tempSensor.objects.values('lowerBound').order_by('-id')[:1]
		currentTempAvg = tempSensor.objects.values('currentTemp').order_by('-id')[:1]
		averageTemp = tempSensor.objects.all().aggregate(Avg('currentTemp'))
		labels = ['Upper Bound', 'Lower Bound', 'Current Temp', 'Average']
		default_items = [currentUpperBound, currentLowerBound, currentTempAvg, averageTemp]
		data = {
			"labels": labels,
			"default": default_items,

		}
		return Response(data)

######form notes######
# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = TempForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('forms')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = TempForm()

#     return render(request, 'index.html', {'form': form})

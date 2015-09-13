#coding=utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
		
@csrf_exempt
def index(request):
	html = open('Backend/index.html', 'r').read()
	return HttpResponse(html)
	#return render_to_response('index.html')
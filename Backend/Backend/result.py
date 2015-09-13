#coding=utf8
import re
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def result(request, name):
	fileID = open('Backend/IDList.txt', 'r')
	page = fileID.read()
	fileID.close()
	dic = {}
	l = page.split('\n')
	for i in l:
		t = i.split(' ')
		dic[t[1]] = t[0]
	t = re.findall(r'/(Backend/static/.*?/.*?\.html)', dic[name])
	file_obj = open(t[0], 'r')
	page = file_obj.read()
	file_obj.close()
	return HttpResponse(page)
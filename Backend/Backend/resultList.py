import os
import re
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response


def merge(l1, l2):
	return list(set(l1) & set(l2))

@csrf_exempt
def resultList(request, offset):
	file1 = open('Backend/InvertedList.txt', 'r')
	page1 = file1.read()
	file1.close()
	file2 = open('Backend/IDList.txt', 'r')
	page2 = file2.read()
	file2.close()

	dic = {}
	l = page1.split('\n')
	for i in l:
		tmp = i.split(' ')
		dic[tmp[0][0:-1]] = []
		for j in range(1, len(tmp)):
			dic[tmp[0][0:-1]].append(tmp[j])
	IDDic = {}
	l = page2.split('\n')
	for i in l:
		tmp = i.split(' ')
		IDDic[tmp[1]] = tmp[0]

	ans = []
	st = ''
	if request.POST.has_key('wd'):
		st = request.POST['wd']
		l = st.split(' ')
		
		S = []
		for i in l:
			if i == '':
				continue
			if dic.has_key(i):
				S.append(dic[i])
			else:
				S.append([])
		if len(S) >= 1:
			ans = reduce(merge, S)

	fatherClass = ''
	father = []
	if request.POST.has_key('select'):
		fatherClass = request.POST['select']
	totalClass = ['', 'cakes', 'cookies']
	for i in totalClass:
		if fatherClass == i:
			father.append({"class": i, "bool": [1]})
		else:
			father.append({"class": i, "bool": []})

	#file_log = open('Backend/log.txt', 'w')
	#file_log.write(request.POST['select'])
	#file_log.close()
	
	ans2 = []
	for i in ans:
		file_obj = open(IDDic[i], 'r')
		page = file_obj.read()
		file_obj.close()
		t = re.findall(r'/static/(.*?)/.*?\.html', IDDic[i])
		if fatherClass == '' or fatherClass == t[0]:
			ans2.append(i)
	ans = ans2

	if ans == []:
		return render_to_response('noResult.html', {'value': st, 'father': father})

	num = (len(ans) - 1) / 15 + 1;
	rg = []
	for i in range(1, num + 1):
		rg.append({'url': '/resultList/%d' % i, 'value': i})

	res = []
	for j in range(len(ans)):
		if j >= int(offset) * 15 - 15 and j < int(offset) * 15:
			i = ans[j]
			file_obj = open(IDDic[i], 'r')
			page = file_obj.read()
			file_obj.close()
			l = re.findall(r'<title>(.*?)</title>', page)
			t = re.findall(r'/(static/.*?/.*?\.html)', IDDic[i])
			url = 'static/' + str(i) + '.html'
			res.append({'title':l[0], 'url':url})

	return render_to_response('list.html', {'resultList': res, 'value': st, 'num': rg, 'father': father})

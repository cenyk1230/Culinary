from HTMLParser import HTMLParser
import re

class MyParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)

	def handle_data(self, data):
		HTMLParser.handle_data(self, data)
		print data
		l = re.findall(r'\b[\w,.]+?\b', data)
		if len(l) != 0:
			print l
		for i in l:
			if dic.has_key(i):
				if not (tmp[1] in dic[i]):
					dic[i].append(tmp[1])
			else:
				dic[i] = [tmp[1]]

	def close(self):
		HTMLParser.close(self)


demo = MyParser()
dic = {}
IDList = open('IDList.txt', 'r').read().split('\n')
for ID in IDList:
	tmp = ID.split(' ')
	page = open(tmp[0], 'r').read()
	l = re.findall(r'<p>[\s\S]*?</p>', '<html><body>' + page + '</body></html>')
	for i in l:
		t = re.sub(r'<span>[\s\S]*</span>', '', i)
		demo.feed(t)
		print ''
print dic
file_obj = open('InvertedList.txt', 'w')
for i in dic:
	st = i + ':'
	for j in dic[i]:
		st += ' ' + j
	file_obj.write(st + '\n')
file_obj.close()
demo.close()

from HTMLParser import HTMLParser
import re

class MyParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)

	def handle_data(self, data):
		HTMLParser.handle_data(self, data)
		file_obj.write(data)
		#print data
		#l = re.findall(r'\b[\w,.]+?\b', data)
		#if len(l) != 0:
		#	print l

	def handle_starttag(self, tag, attrs):
		if tag == 'p':
			file_obj.write('<p>')
		elif tag == 'h2':
			file_obj.write('<h2>')

	def handle_endtag(self, tag):
		if tag == 'p':
			file_obj.write('</p>\n')
		elif tag == 'h2':
			file_obj.write('</h2>')

	def close(self):
		HTMLParser.close(self)


demo = MyParser()

prefix = '''
<style type="text/css">
	img{
		opacity: 0.6;
	}
</style>
'''

background = '''<div id="Layer1" style="position:fixed; width:100%; height:100%; z-index:-1">
<img src="http://img.taopic.com/uploads/allimg/120301/2195-12030112135854.jpg" height="100%" width="100%"/>
</div>\n'''

IDList = open('IDList.txt', 'r').read().split('\n')
for ID in IDList:
	tmp = ID.split(' ')
	file_name = tmp[0].replace('HTML', 'static')
	file_name = file_name.decode().encode('utf8')
	print file_name
	file_obj = open(file_name, 'w')
	page = open(tmp[0], 'r').read()
	title = re.findall(r'<h1 id="firstHeading"\s*class="firstHeading"\s*lang="en">(.*?)</h1>', page)
	file_obj.write('<h1>' + title[0] + '</h1>')
	l = re.findall(r'<p>[\s\S]*?</p>|<h2>[\s\S]*?</h2>', '<html><body>' + page + '</body></html>')
	#print l
	for i in l:
		t = re.sub(r'<span>[\s\S]*</span>', '', i)
		t = re.sub(r'<span class="mw-editsection"><span class="mw-editsection-bracket">[\s\S]*?</span></span>', ' ', t)
		demo.feed(t)
		print ''
	file_obj.close()

	file_obj = open(file_name, 'r')
	context = file_obj.read()
	file_obj.close()
	context = context.replace('<p></p>', '')
	context = context.replace('<h2>Contents</h2>', '')
	#while context[-1] == '\n':
	#	context = context[0:-1]
	context = re.sub(r'\n{2,}', '\n', context)
	context = re.sub(r'[\n\r\s]*$', '', context)
	context = re.sub(r'(<h2>.*?</h2>(\n)*?){2,}', '', context)
	
	context = re.sub(r'<h2>.*?</h2>$', '', context)
	context = context.replace('</h1>', '</h1>\n')
	context = context.replace('</h2>', '</h2>\n')
	context = re.sub(r'\n{2,}', '\n', context)
	context = '<html>\n<head>\n<meta charset="UTF-8" />\n<title>%s</title>\n' % title[0] + prefix + '</head>\n<body>\n' + background + context + '\n</body>\n</html>'
	#print context
	file_obj = open(file_name, 'w')
	file_obj.write(context)
	file_obj.close()
	


demo.close()

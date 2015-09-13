import re
import urllib
import urllib2

def getHtml(url):
	request = urllib2.Request(url)
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	#headers = {'User-Agent' : user_agent}
	request.add_header('User-Agent', 'fake-client')
	response = urllib2.urlopen(request)
	page = response.read()
	return page

def getList(page):
	page = re.sub('\n+', '', page)
	reg = r'<table\s*class\s*=\s*"wikitable.*</table>'
	print 'reg=',reg
	st = re.findall(reg, page)
	print 'st=',st
	reg2 = r'<tr><td><a\s*href\s*=\s*"(.*?)".*?</a></td>'
	hrefList = re.findall(reg2, st[0])
	return hrefList

url = 'https://en.wikipedia.org/wiki/List_of_cookies'
page = getHtml(url)
#page_file = open('result.html', 'w')
#page_file.write(page)
#page_file.close()
hrefList = getList(page)
for ref in hrefList:
	totalRef = 'https://en.wikipedia.org' + ref
	print totalRef
	name = re.match(r'/wiki/(.*)', ref)
	if name:
		t = name.group()
		print t[6:]
		page_file = open('/Users/Roger/Projects/Culinary/cookies/' + t[6:] + '.html', 'w')
		new_page = getHtml(totalRef)
		page_file.write(new_page)
		page_file.close()

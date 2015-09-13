import os
def walk_dir(dir, fileinfo, topdown=True):
	tot = 1;
	for root, dirs, files in os.walk(dir, topdown):
		for name in files:
			if name[0] != '.':
				print(os.path.join(root, name))
				fileinfo.write(os.path.join(root,name)+ ' ' + '%d' % tot + '\n')
				tot = tot + 1

dir = raw_input('please input the path:')
fileinfo = open('IDList.txt', 'w')
walk_dir(dir, fileinfo)
fileinfo.close()
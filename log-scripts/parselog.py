import os
import matplotlib.pyplot as plt

def dummy(filename):
	infolist = []
	debuglist = []
	errlist = []
	icountL = []
	dcountL = []
	ecountL = []
	try:
		log = open(filename, 'r')
	except IOError:
		print 'File does not exist'
	for line in log:
		data = line.split()
		n = len(data)
                if n < 1:
                        break
		identifier = data[4]
		tag = data[5]
		if identifier == 'I':
			if tag in infolist:
				ind = infolist.index(tag)
				icountL[ind] += 1
			else:
				infolist.append(tag)
				icountL.append(1)
		elif identifier == 'D':
			if tag in debuglist:
				ind = debuglist.index(tag)
				dcountL[ind] += 1
			else:
				debuglist.append(tag)
				dcountL.append(1)
		elif identifier == 'E':
			if tag in errlist:
				ind = errlist.index(tag)
				ecountL[ind] += 1
			else:
				errlist.append(tag)
				ecountL.append(1)
	log.close()
	print 'List of unique info tags is as follows:'
	print infolist, icountL
	print 'List of unique debug tags is as follows:'
	print debuglist, dcountL
	print 'List of unique error tags is as follows:'
	print errlist, ecountL
	plt.pie(icountL, explode=None, labels=infolist)


def forall(path):
	infolist = []
	deblist = []
	errlist = []
	warnlist = []
	nlines = 0
	icountL = []
	dcountL = []
	ecountL = []
	wcountL = []
	fileList = [os.path.join(path, fi) for fi in os.listdir(path)]
	for f in fileList:
		print 'File currently scanned is ' + f
		try:
			log = open(f, 'r')
		except IOError:
			print 'File doesnot exist'
			break
		for line in log:
                	data = line.split()
                	n = len(data)
                	if n < 5:
				print line
                        	break
                	identifier = data[4]
                	tag = data[5]
                	if identifier == 'I':
                        	if tag in infolist:
                                	ind = infolist.index(tag)
                                	icountL[ind] += 1
                        	else:
                                	infolist.append(tag)
                                	icountL.append(1)
                	elif identifier == 'D':
                        	if tag in deblist:
                                	ind = deblist.index(tag)
                                	dcountL[ind] += 1
                        	else:
                                	deblist.append(tag)
                                	dcountL.append(1)
                	elif identifier == 'E':
                        	if tag in errlist:
                                	ind = errlist.index(tag)
                                	ecountL[ind] += 1
                        	else:
                                	errlist.append(tag)
                                	ecountL.append(1)
			elif identifier == 'W':
                                if tag in warnlist:
                                        ind = warnlist.index(tag)
                                        wcountL[ind] += 1
                                else:
                                        warnlist.append(tag)
                                        wcountL.append(1)

        	log.close()
		print 'Scan over for ' + f
#	print 'List of unique info tags is as follows:'
#	for i in range(0,len(infolist)):
#		print infolist[i] , icountL[i]
	log = open('/home/anudipa/logs/summary.log', 'w')
	log.write('List of unique info tags for %s\n\n' % path)
	for i in xrange(0,len(infolist)):
		log.write('%s %d\n' % (infolist[i], icountL[i]))

	log.write('\nList of unique debug tags for %s\n\n' % path)
	for i in xrange(0,len(deblist)):
                log.write('%s %d\n' % (deblist[i], dcountL[i]))

	log.write('\nList of unique error tags for %s\n\n' % path)
	for i in xrange(0,len(errlist)):
                log.write('%s %d\n' % (errlist[i], ecountL[i]))

	log.write('\nList of unique warn tags for %s\n\n' % path)
	for i in xrange(0,len(warnlist)):
                log.write('%s %d\n' % (warnlist[i], wcountL[i]))

	log.close()
#	get top 10 tags from each group	
	print infolist[icountL.index(max(icountL))]
	c = 0
	index = []
	row = []
	for i in icountL:
		if i > 200:
			j = icountL.index(i)
			index.append(infolist[icountL.index(i)])
			index.append(i)
	for i in range(0,len(index),2):
        	print index[i], index[i+1]
	
#	print 'list of unique debug tags is as follows:'
#	print deblist
#	print 'List of unique error tags is as follows:'
#	print errlist


def getLinesforTag(path,keyword):
	name = keyword + '.txt'
	fname = os.path.join(path,name)
	try:
		myfile = open(fname,'w')
	except IOError:
		print 'Cannot open myfile'
		return 0
	for root,dirs,files in os.walk(path):
		filelist = []
		for name in files:
			filelist.append(os.path.join(root,name))
		filelist.sort(key=os.path.getmtime)
		print 'Checking ----> ',root
	        for f in filelist:
        	        try:
                	        log = open(f, 'r')
	                except IOError:
        	                print 'File doesnot exist'
                	        break
	                for line in log:
        	                data = line.split()
                	        n = len(data)
                        	if n < 6:
                                	pass
	                        else:
        	                	identifier = data[4]
                	        	tag = data[5]
					if tag.startswith(keyword):
						myfile.write(line)
						myfile.write('\n')
			log.close()
	
	print '---------Done-------------'
	myfile.close()


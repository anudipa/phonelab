import os
from numpy import arange
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime 

def dummy(path, keyword):
	for root,dirs,files in os.walk(path):
		for name in files:
			filename = os.path.join(root,name)
			print filename
			status = os.stat(filename)
			print status




def batteryprof1(path):
	filelist = []
	time = []
	date = []
	stats = []

	for root,dirs,files in os.walk(path):
		for name in files:
			filelist.append(os.path.join(root,name))
	filelist.sort(key=os.path.getmtime)
	for filename in filelist:
		try:
			log = open(filename,'r')
		except IOError:
			print 'File doesnot exit'
			break
		for line in log:
			data = line.split()
			n = len(data)
			if n < 6:
				print line + filename
			else:
				tag = data[5]
				if tag.startswith('PowerUI') and data[7].startswith('updating'):
					t1 = data[1].split(':')
					sec = t1[2].split('.')
					t = int(t1[0])*60*60 + int(t1[1])*60 + int(sec[0])
					time.append(t)
					date.append(data[0])
					temp = (data[11].split('='))[1]
					stats.append(int(temp))
		log.close()
	
#	fig = plt.figure()
	x = []
	y = []
	temp = date[0]
	for i in xrange(0,len(stats)):
		if (i == 0) or (temp==date[i]):
			x.append(time[i])
			y.append(stats[i])
		if (stats[i] == 0) or (temp!=date[i]):
			print 'Plotting line'
			plt.plot(x,y,label='%s' % temp)
			x = []
			y = []
			temp = date[i+1]	
	plt.grid()
	plt.legend()
#	fig.suptitle('Plot of battery draining on each date', fontsize=12)
	plt.show()



def batteryprof(path):
        filelist = []
        timestamp = []
        stats = []

        for root,dirs,files in os.walk(path):
                for name in files:
                        filelist.append(os.path.join(root,name))
        filelist.sort(key=os.path.getmtime)
        for filename in filelist:
                try:
                        log = open(filename,'r')
                except IOError:
                        print 'File doesnot exit'
                        break
                for line in log:
                        data = line.split()
                        n = len(data)
                        if n < 6:
                                print line + filename
                        else:
                                tag = data[5]
                                if tag.startswith('PhoneLab-StatusMonitorBattery') and data[6].startswith('Battery'):
					newdate = data[0] + '-12 ' + data[1]
                                        t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
                                        timestamp.append(t)
                                        temp = data[7]
                                        stats.append(int(temp))
        	log.close()
	n = len(stats)
	print n
#       fig = plt.figure()
        x = []
        y = []
        for i in xrange(0,len(stats)):
		x.append(timestamp[i])
		y.append(stats[i])
	plt.plot(x,y)
	plt.xticks(rotation=45)
        plt.grid()
#	plt.legend()        
	plt.title('Plot of battery level ' , fontsize=12)
        plt.show()


def dalvikprof(path):
	date = []
	timestamp = []
	filelist = []
	for root,dirs,files in os.walk(path):
                for name in files:
                        filelist.append(os.path.join(root,name))
        filelist.sort(key=os.path.getmtime)
        for filename in filelist:
                try:
                        log = open(filename,'r')
                except IOError:
                        print 'File doesnot exit'
                        break
                for line in log:
                        data = line.split()
                        n = len(data)
                        if n < 6:
#                                print line + filename
				continue
                        else:
                                tag = data[5]
                                if tag.startswith('dalvikvm'):
					if data[0].startswith('01-') or data[0].startswith('12'):
						print 'Check this ---------->' + filename + data[0]
					else:
						newdate = data[0] + '-12 ' + data[1]
        	                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
						timestamp.append(t)
#			if data[0].startswith('01-') or data[0].startswith('02'):
#						print 'Check this ---------->' + filename + data[0]
		log.close()
	x = []
	y = []
	c = 0
	temp = timestamp[0].date()
	print temp
	print len(timestamp)
#	print timestamp[1:10]
	for i in xrange(1,len(timestamp)):
		latest = timestamp[i].date()
                if temp==latest:
			c +=1
		else:
                        x.append(timestamp[i-1])
			y.append(c)
			c = 0
			temp = latest
#	count = arange(0,len(timestamp))
#	print count[1:10]
#	plt.plot(timestamp,count)
	print y[1:100]
	plt.plot(x,y,marker='o')
#	print len(x), max(y), min(y)
#			x = []
#                        y = []
#                        temp = date[i]
#			x.append(time[i])
#			y.append(time.count(time[i]))                        
        plt.grid()
#       plt.legend()        
        plt.title('Plot of  dalvik', fontsize=12)
	plt.xticks(rotation=45)
	plt.tight_layout()
        plt.show()


def chargeprof(path):
	fname = os.path.join(path,'hist.pdf')
	for root,dirs,files in os.walk(path):
		pp = PdfPages(fname)
		stats = []
		timestamp = []
		filelist = []
		print fname
#		print dirs
#		print files
		for name in files:
			filelist.append(os.path.join(root,name))
		filelist.sort(key=os.path.getmtime)
#	name = open('/home/anudipa/logs/BatteryLogs.log','w')
	        for filename in filelist:
			try:
				log = open(filename,'r')
	                except IOError:
       		                print 'File doesnot exit'
               		        break
	                for line in log:
       		                data = line.split()
               		        n = len(data)
                       		if n < 6:
#                               		print line + filename
					continue
	                        else:
       		                        tag = data[5]
               		                if tag.startswith('PhoneLab-StatusMonitorBattery') and data[6].startswith('Battery'):
#					name.write(line)
#					name.write('\n')
						newdate = data[0] + '-12 ' + data[1]
                               		        t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
                                       		timestamp.append(t)
                                        	temp = data[7]
        	                                stats.append(int(temp))
			log.close()
#	name.close()
		x = []
		y = []

		for i in xrange(1,len(stats)-2):
			if stats[i] < stats[i+1] and stats[i] < stats[i-1]:
				x.append(timestamp[i])
				y.append(stats[i])
		print y
		if len(y) > 0:
			plt.hist(y,bins=10, label = root)

#	print stats[i], timestamp[i]
#	plt.plot(timestamp,stats)
#			plt.plot(x,y)
#		plt.hist(y)
#			plt.xticks(rotation=45)
		plt.grid()
		plt.title('Charge left before plugging over time')
		plt.tight_layout()
#		plt.legend()
#			plt.show()
		plt.savefig(pp, format='pdf')
#		plt.figure.clear()
	pp.close()

			

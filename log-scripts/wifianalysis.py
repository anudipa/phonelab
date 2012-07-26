import os
from numpy import arange
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
from datetime import datetime


def analyse(path):
#Define the names and the path of the file where graphs will be stored
        fname1 = os.path.join(path,'wifisignal.pdf')
        pp1 = PdfPages(fname1)
        c = 0
        cmap1 = mpl.cm.autumn
        cmap2 = mpl.cm.winter
#Debug file has a debugging purposes
        debug = open(os.path.join(path,'wificheck.txt'), 'w')
        for root,dirs,files in os.walk(path):
                stats = []
                timestamp = []
                filelist = []
		dictionary = {}
		dates = []
#       print fname
#               print dirs
#               print files
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
                                if n < 10 or data[0].startswith('01') or data[0].startswith('12'):
#                                               print line + filename
                                        continue
                                else:
                                        tag = data[5]
# when collecting signal strength for given tag
                                        if tag.startswith('PhoneLab-StatusMonitorSignal') and data[6].startswith('Signal_Strength'):
						temp = data[7]
						newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
						if len(timestamp) == 0:
                                                        timestamp.append(t)
                                                        stats.append(int(temp))
                                                elif timestamp[-1] < t:
                                                        timestamp.append(t)
                                                        stats.append(int(temp))
                                                elif timestamp[0] > t:
                                                        timestamp.insert(0,t)
                                                        stats.insert(0,int(temp))
                                                else:
                                                        for j in xrange(0,len(timestamp)-2):
                                                                if timestamp[j] < t and timestamp[j+1] > t:
                                                                        timestamp.insert(j+1,t)
                                                                        stats.insert(j+1,int(temp))

# when calculating number of times device connected to a bssid each day
					if tag.startswith('PhoneLab-WiFiReceiver') and data[6].startswith('SSID'):
						debug.write('SSID: %s   BSSID: %s\n' % (data[7],data[9]))
						newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
						dictionary[t]=data[9]

		log.close()
#************ GRAPH PLOTTING SECTION ***********************

		c = c+1		#c -> figure number, each device will have distinct graph
#Getting device name from the path
                device = root.split('/')

#Graph for wifi signals normalised over each hour
		t = []
                s = []
                temp = 0
                count = 0
#                debug.write('Normalised wifi signals ---> %s\n' % root)
                if len(timestamp) > 0:
                        current = timestamp[0]
                        for i in xrange(1,len(timestamp)-1):
                                if timestamp[i].hour==current.hour:
                                        temp += stats[i]
                                        temp = temp / 2
                                else:
                                        t.append(timestamp[i-1])
                                        s.append(temp)
                                        current = timestamp[i]
#                                       debug.write('%s : %s \n' % (t[-1],s[-1]))
                        t.append(timestamp[i])
                        s.append(temp)

		if len(s) > 0:
			fig1 = figure(c, dpi=10)
			plot(t,s,color=cmap1(0.5),marker='o')
			grid()
			title('Wifi Signals received by %s' % device[-1], fontsize=12)
			xlabel('Time', fontsize=12)
			ylabel('Signal Strength in dB', fontsize=12)
			pp1.savefig(fig1)
			close()
			fig1.clear()

#Graph for plotting number of times a device connected to each BSSID each day
#Step 1 : count number of times bssid appeared for each unique date
		for item in dictionary:
			debug.write('%s : %s\n' % (item, dictionary[item]))
			print item, dictionary[item]
		for key, item in dictionary.iteritems():
			if len(date) == 0
				date.append(key)
			elif date.count(key.date()) > 0:
				

#losing the files that are open
	pp1.close()
	debug.close()

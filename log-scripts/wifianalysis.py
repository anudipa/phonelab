import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
from datetime import datetime
from collections import defaultdict

def analyse(path):
#Define the names and the path of the file where graphs will be stored
        fname1 = os.path.join(path,'wifisignal.pdf')
	fname2 = os.path.join(path,'wifibssid.pdf')
	fname3 = os.path.join(path, 'wifibssid1.pdf')
        pp1 = PdfPages(fname1)
	pp2 = PdfPages(fname2)
	pp3 = PdfPages(fname3)
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
	
		bssid = []
		dict_ = defaultdict(list)
		dict2 = defaultdict(list)
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
						#debug.write('SSID: %s   BSSID: %s\n' % (data[7],data[9]))
						newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
						key = data[9]
						dict_[key].append(t.date())
						dict2[t.date()] = key
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
			col = np.random.random(len(dict_))	
#			print col
			fig2 = figure(c, dpi=10)
			for item in dict_:
				debug.write('%s : %s\n' % (item, dict_[item]))
				current = list(dict_[item])
				dates = []
				new_count = []
#				print item
				for i in xrange(0,len(current)):
					if len(dates) == 0 or dates.count(current[i]) == 0:
						dates.append(current[i])
						new_count.append(current.count(dates[-1]))
#					else:
#						index = dates.index(current[i])
#						new_count[index] += 1				
				
				plot(dates,new_count, '--o', label=item)
				grid()
				legend(handlelength=10)
			title('Number of times %s connects to different BSSID' % device[-1])
			xlabel('Time', fontsize=15)
			ylabel('Number of times', fontsize=15)
			pp2.savefig(fig2)
			close()
			fig2.clear()
			
#Graph for visualising total number of connections to access points per device
		
		if len(dict2) > 0:
			x = []
			y = []
			fig3 = figure(c,dpi=10)
			for item in dict2:
				current = list(dict2[item])
				bssid_count = len(current)
				y.append(bssid_count)
				x.append(item)
			bar(x,y,width=.5, color = cmap1(0.4))
			title('Number of access points %s connects to each day' % device[-1])
			pp3.savefig(fig3)
			close()
			fig3.clear()
#Graph for visualising total number of connections to AP where consecutive coonections to same AP are discarded
		if len(dict2) > 0:
			x = []
			y = []
			fig4 = figure(c,dpi=10)
			for item in dict2:
				current = list(dict2[item])
				bssid_count = 0
				for i in xrange(0,len(current)):
					if i == 0 or current[i] != current[i-1]:
						bssid_count += 1
				y.append(bssid_count)
				x.append(item)
			plot(x,y,'--o',color = cmap1(0.8))
			title('Visualising possible movement of %s each day' % device[-1])
			xlabel('Time', fontsize=15)
			ylabel('Number of coonections', fontsize=15)
			pp3.savefig(fig4)
			close()
			fig4.clear()

#Graph for visualising in one day a device changes how many access point

#Graph for visualing in each day different devicse connect to how many access points
				

#Closing the files that are open
	pp1.close()
	pp2.close()
	pp3.close()
	debug.close()

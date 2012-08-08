import os
import numpy as np
import matplotlib as mpl
from matplotlib.dates import WeekdayLocator, DateFormatter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
from datetime import datetime, timedelta
from collections import defaultdict

#Global colormaps
cmap1 = mpl.cm.autumn
cmap2 = mpl.cm.winter
cmap3 = mpl.cm.hsv


#Generate graph for wifi signal strength received by a device
def signalplot(path):
	d = os.path.join(path,'wifi')
	if not os.path.exists(d):
		os.makedirs(d)
	fname = os.path.join(d,'wifisignal.pdf')
	pp = PdfPages(fname)
	c = 0
	for root,dirs,files in os.walk(path):
		stats = []
		timestamp = []
		filelist = []
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
			log.close()
#************************Plotting Graph***********************************
		c = c +1
		device = root.split('/') # to find device name from given path

		t = []
                s = []
                temp = 0
                count = 0
                if len(timestamp) > 0:
                        current = timestamp[0]
                        for i in xrange(1,len(timestamp)-1):
                                if timestamp[i].hour==current.hour:	#average signal strength in each hour
                                        temp += stats[i]
                                        temp = temp / 2
                                else:
                                        t.append(timestamp[i-1])
                                        s.append(temp)
                                        current = timestamp[i]
                        t.append(timestamp[i])
                        s.append(temp)

                if len(s) > 0:
                        fig = figure(c, dpi=10)
                        plot(t,s,color=cmap1(0.5),marker='o')
                        grid()
                        title('Wifi Signals received by %s(normalised over each hr)' % device[-1], fontsize=12)
                        xlabel('Time', fontsize=12)
                        ylabel('Signal Strength in dB', fontsize=12)
                        pp.savefig(fig)
                        close()
                        fig.clear()
	pp.close()



def signaldata(path):
	signaldict = defaultdict(defaultdict)
	for root,dirs,files in os.walk(path):
                device = root.split('/')
		key = device[-1]
		filelist = []
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
						signaldict[key][t].append(temp)

                        log.close()
	return signaldict

#Plot the number of times a device connects to an access point over time
def bssidcountplot(path):
	d = os.path.join(path,'wifi')
        if not os.path.exists(d):
                os.makedirs(d)
        fname = os.path.join(d,'bssidcount.pdf')
        pp = PdfPages(fname)
        c = 0				#count for figures
        for root,dirs,files in os.walk(path):
		filelist = []
		dict_ = defaultdict(list)
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
					if tag.startswith('PhoneLab-WiFiReceiver') and data[8].startswith('BSSID'):
                                                newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
                                                key = data[9]
                                                dict_[key].append(t.date())
			log.close()
		c = c+1
		device = root.split('/')	#to get name of the device from the given path

		if len(dict_) > 0:
                        col = np.random.random(len(dict_))
			newdict = defaultdict(lambda:defaultdict(int))
                        fig = figure(c, dpi=10)
			ax = subplot(111)
                        for item in dict_:
                                current = list(dict_[item])
                                dates = []
                                new_count = []
                                for i in xrange(0,len(current)):
                                        if len(dates) == 0 or dates.count(current[i]) == 0:
                                                dates.append(current[i])
                                                new_count.append(current.count(dates[-1]))
#						print 'Abt to do it'
						newdict[item][dates[-1]]=new_count[-1]
			mx = 0
			mn = 500
			for item1 in newdict:
				temp1 = 0
				temp2 = 0
				for item2 in newdict[item1]:
					if temp1 < newdict[item1][item2]:
						temp1 = newdict[item1][item2]
					if temp2 > newdict[item1][item2]:
						temp2 = newdict[item1][item2]
				if mx < temp1:
					mx = temp1
				if mn > temp2:
					mn = temp2
			print mx, mn
			for item1 in newdict:
				flag = 0
				for item2 in newdict[item1]:
					if newdict[item1][item2] > (mx-mn)/2:
						flag = 1
						break
				if flag == 1:
					print item1,'\n',newdict[item1].keys(),newdict[item1].values(), '\n'
					ax.plot(newdict[item1].keys(),newdict[item1].values(), '.',markersize=15, label=item1)

                        grid()
#                        legend(loc='best',bbox_to_anchor=(1.13,1.08))
			box = ax.get_position()
			ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

			# Put a legend below current axis
			ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=5)
                        title('Number of times %s connects to a particular BSSID' % device[-1])
#                        xlabel('Time', fontsize=15)
                        ylabel('Number of times', fontsize=15)
                        pp.savefig(fig)
                        close()
                        fig.clear()
	pp.close()


def bssidcountdata(path):
	bssiddict = defaultdict(lambda:defaultdict(defaultdict))
	for root,dirs,files in os.walk(path):
                filelist = []
                device = root.split('/')
		dict_ = defaultdict(list)
		key = device[-1]
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
                                        if tag.startswith('PhoneLab-WiFiReceiver') and data[8].startswith('BSSID'):
                                                newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
                                                dict_[data[9]].append(t.date())
                        log.close()
		if len(dict_) > 0:
			for item in dict_:
				current = list(dict_[item])
				dates = []
				new_count = []
				for i in xrange(0,len(current)):
					if len(dates) == 0 or dates.count(current[i]) == 0:
						bssiddict[key][item][current[i]].append(current.count(dates[-1]))
	return bssiddict

def bssiddata(path):
	bssiddict = defaultdict(lambda:defaultdict(defaultdict))
        for root,dirs,files in os.walk(path):
                filelist = []
                device = root.split('/')
                dict_ = defaultdict(list)
                key = device[-1]
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
                                        if tag.startswith('PhoneLab-WiFiReceiver') and data[8].startswith('BSSID'):
                                                #debug.write('SSID: %s   BSSID: %s\n' % (data[7],data[9]))
                                                newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
                                                dict_[data[9]].append(t)
                        log.close()
                if len(dict_) > 0:
                        for item in dict_:
                        	bssiddict[key][item].append(dict_[item])
	return bssiddict

def conxncountbar(path):
        d = os.path.join(path,'wifi')
        if not os.path.exists(d):
                os.makedirs(d)
        fname = os.path.join(d,'totalconxn.pdf')
        pp = PdfPages(fname)
        c = 0                           #count for figures
        for root,dirs,files in os.walk(path):
                filelist = []
                dict_ = defaultdict(list)
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
                                        if tag.startswith('PhoneLab-WiFiReceiver') and data[8].startswith('BSSID'):
                                                newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
                                                dict_[t.date()].append(data[9])
                        log.close()
                c = c+1
                device = root.split('/')        #to get name of the device from the given path

                if len(dict_) > 0:
                        x = []
                        y = []
                        fig1 = figure(c,dpi=10)
                        for item in dict_:
                                current = list(dict_[item])
                                bssid_count = len(current)
                                y.append(bssid_count)
                                x.append(item)
                        bar(x,y,width=.5, color = cmap1(0.4))
                        title('Number of access points %s connects to each day' % device[-1])
                        pp.savefig(fig1)
                        close()
                        fig1.clear()
		if len(dict_) > 0:
                        x = []
                        y = []
                        fig2 = figure(c,dpi=10)
                        for item in dict_:
                                current = list(dict_[item])
                                bssid_count = 0
                                for i in xrange(0,len(current)):
					if i == 0 or current[i] != current[i-1]:
                                                bssid_count += 1
                                y.append(bssid_count)
                                x.append(item)
                        bar(x,y,color = cmap1(0.8))
                        title('Number of large movements by %s each day----> less height = less movement' % device[-1])
                        xlabel('Time', fontsize=15)
                        ylabel('Number of connections', fontsize=15)
                        pp.savefig(fig2)
                        close()

	pp.close()

	
def weeklyplot(path):
	d = os.path.join(path,'wifi')
        if not os.path.exists(d):
                os.makedirs(d)
        fname = os.path.join(d,'weeklyconxn.pdf')
        pp = PdfPages(fname)
        c = 0                           #count for figures
        for root,dirs,files in os.walk(path):
                filelist = []
                dict_ = defaultdict(list)
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
                                        if tag.startswith('PhoneLab-WiFiReceiver') and data[8].startswith('BSSID'):
                                                newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
                                                dict_[t.date()].append(data[9])
                        log.close()
                c = c+1
                device = root.split('/')        #to get name of the device from the given path

		if len(dict_) > 0:
                                num = 10
                                x = []
                                y = []
                                for item in dict_:
                                        current = list(dict_[item])
                                        bssid_count = 0
                                        for i in xrange(0,len(current)):
                                                if i == 0 or current[i] != current[i-1]:
                                                        bssid_count += 1

                                        if len(x) == 0 or item > x[-1]:
                                                x.append(item)
                                                y.append(bssid_count)
                                        elif item < x[0]:
                                                x.insert(0,item)
                                                y.insert(0,bssid_count)
                                        else:
                                                for n in xrange(len(x)-1,1):
                                                        if item < x[n] and item > x[n-1]:
                                                                x.insert(n,item)
                                                                y.insert(n,bssid_count)
                                                                break
                                flag = 0
                                col = random()
                                for i in xrange(0, len(x)):

                                        if x[i] - x[flag] >= timedelta(days=6):
                                                num += 2
                                                fig1 = figure(c,dpi=10)
                                                ax = fig1.add_subplot(111)
                                                m = i+1
                                                ax.bar(x[flag:m],y[flag:m], width=.35, color = cmap2(col))
                                                title('From %s-%s -- %s' % (x[flag],x[i],device[-1]))
                                                xlabel('Time', fontsize=15)
                                                ylabel('Number of connections', fontsize=15)
                                                ax.xaxis.set_major_locator(WeekdayLocator(byweekday = (MO,TU,WE,TH,FR,SA)))
                                                ax.xaxis.set_major_formatter(DateFormatter('%A \n%d %b'))

                                                m = i+1
                                                flag = i+1
                                                pp.savefig(fig1)
                                                close()
                                                fig1.clear()

	pp.close()

def ssidplot(path):
	d = os.path.join(path,'wifi')
        if not os.path.exists(d):
                os.makedirs(d)
        fname = os.path.join(d,'ssidperc.pdf')
        pp = PdfPages(fname)
        c = 0                           #count for figures
        for root,dirs,files in os.walk(path):
                filelist = []
                dict1 = defaultdict(list)
		dict2 = defaultdict(list)
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
                                        if tag.startswith('PhoneLab-WiFiReceiver') and data[8].startswith('BSSID'):
                                                newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
						key = data[9]
		                                dict1[t.date()].append(key)
                                                ssid = data[7]
                                                if len(dict2[ssid]) == 0:
                                                        dict2[ssid].append(key)
                                                try:
                                                        dict2[ssid].index(key)
                                                except ValueError:
                                                        dict2[ssid].append(key)
			log.close()
                c = c+1
                device = root.split('/')        #to get name of the device from the given path
                names = []
                for item in dict2:
                        names.append(item)

		if len(dict1) > 0 and len(dict2) > 0:
                        x = []
                        y = []
                        p = []
                        stats = defaultdict(list)
                        num = [0]*len(names)
                        n = 0
                        fig = figure(c,dpi=10)
                        for item in dict1:
                                current = list(dict1[item])
                                for i in xrange(0,len(current)):
                                       if i == 0 or current[i] != current[i-1]:
                                                for key in dict2:
                                                        l = list(dict2[key])
                                                        try:
                                                                if l.index(current[i]) >= 0:
                                                                        num[names.index(key)] +=1
                                                                        break
                                                        except ValueError:
                                                                continue
                                for j in xrange(0, len(names)):
                                        stats[names[j]].append(num[j])

                                x.append(item)
                        for key in stats:
                                bar(x,stats[key],color = cmap3(random()))
                                print key
                        legend(names)
                        title('Contribution of different network -- %s' % device[-1])
                        xlabel('Time', fontsize=15)
                        ylabel('Number of connections', fontsize=15)
                        pp.savefig(fig)
                        close()

	pp.close()

def ssidtobssid(path):
	dict_ = defaultdict(list)
	for root,dirs,files in os.walk(path):
                filelist = []
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
                                        if tag.startswith('PhoneLab-WiFiReceiver') and data[8].startswith('BSSID'):
						if len(dict_[data[7]]) == 0:
                                                        dict_[data[7]].append(data[9])
                                                try:
                                                        dict_[data[7]].index(data[9])
                                                except ValueError:
                                                        dict_[data[7]].append(data[9])
			log.close()
	return dict_

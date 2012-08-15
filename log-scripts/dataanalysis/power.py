import os
from numpy import arange
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
from datetime import datetime, timedelta
from collections import defaultdict


cmap1 = mpl.cm.autumn
cmap2 = mpl.cm.winter

#get graph for varying battery level over time for each device
def batterylevelplot(path):
        d = os.path.join(path,'power')
        if not os.path.exists(d):
                os.makedirs(d)
	fname = os.path.join(d,'batterylevel.pdf')
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
                                if n < 6 or data[0].startswith('01') or data[0].startswith('12'):
                                        continue
                                else:
                                        tag = data[5]

                                        if tag.startswith('PhoneLab-StatusMonitorBattery') and data[6].startswith('Battery'):
                                                temp = data[7]
# Putting the timestamp in the correct position in the array by checking against all the variables in the aray
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
#*****************GRAPH PLOTTING SECTION *******************

                c = c+1         #different figure for different devices, c ----> figure number
#Getting device name from the path
                device = root.split('/')

#Graph for showing battery level over time for each device
                if len(stats) > 0:
                        fig1 = figure(c, dpi=15 )
                        plot(timestamp,stats,color = cmap2(random()),marker='o')
                        grid()
                        xlabel('Time',fontsize=15)
                        ylabel('Battery Level',fontsize=15)
                        title('Battery level for %s' % device[-1], fontsize=20)
                        pp.savefig(fig1)
                        close()
                        fig1.clear()



	pp.close()


def getbatterylevel(path):
	batterydata = defaultdict(int)
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
                                if n < 6 or data[0].startswith('01') or data[0].startswith('12'):
                                        continue
                                else:
                                        tag = data[5]

                                        if tag.startswith('PhoneLab-StatusMonitorBattery') and data[6].startswith('Battery'):
                                                temp = data[7]

                                                newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')

						batterydata[t] = int(temp)
#						print 'Inserted',batterydata[t]
                        log.close()
	return batterydata

def getlowlevel(path):
	lowdata = defaultdict(int)
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
                                if n < 6 or data[0].startswith('01') or data[0].startswith('12'):
                                        continue
                                else:
                                        tag = data[5]

                                        if tag.startswith('PowerUI') and data[7].startswith('updating'):
                                                temp = (data[11].split('='))[1]
                                                newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
						lowdata[t] = int(temp)
		log.close()
	return lowdata


def levelbyhrplot(path):
        d = os.path.join(path,'power')
        if not os.path.exists(d):
                os.makedirs(d)
        fname = os.path.join(d,'levelovrhr.pdf')
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
                                if n < 6 or data[0].startswith('01') or data[0].startswith('12'):
                                        continue
                                else:
                                        tag = data[5]

                                        if tag.startswith('PhoneLab-StatusMonitorBattery') and data[6].startswith('Battery'):
                                                temp = data[7]
# Putting the timestamp in the correct position in the array by checking against all the variables in the aray
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
#*****************GRAPH PLOTTING SECTION *******************

                c = c+1         #different figure for different devices, c ----> figure number
#Getting device name from the path
                device = root.split('/')

#Graph for battery level normalised by hour for each day fo each device
                t = []
                s = []
                temp = 0
                count = 0
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
                        t.append(timestamp[i])
                        s.append(temp)
                if len(s) > 0:
#                       print s
                        fig = figure(c,dpi=10)
                        plot(t,s,color=cmap2(random()),marker='o')
                        grid()
                        title('Normalised Battery Level for %s' % device[-1], fontsize=15)
                        xlabel('Time', fontsize=15)
                        ylabel('Battery Level', fontsize=15)
                        pp.savefig(fig)
                        fig.clear()
                        close()


	pp.close()


#Graph for showing battery level before phone is plugged in
def pluginplot(path):
        d = os.path.join(path,'power')
        if not os.path.exists(d):
                os.makedirs(d)
        fname = os.path.join(d,'levelovrhr.pdf')
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
                                if n < 6 or data[0].startswith('01') or data[0].startswith('12'):
                                        continue
                                else:
                                        tag = data[5]

                                        if tag.startswith('PhoneLab-StatusMonitorBattery') and data[6].startswith('Battery'):
                                                temp = data[7]
# Putting the timestamp in the correct position in the array by checking against all the variables in the aray
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
#*****************GRAPH PLOTTING SECTION *******************

                c = c+1         #different figure for different devices, c ----> figure number
#Getting device name from the path
                device = root.split('/')

                y = []
                for i in xrange(1,len(stats)-2):
                        if stats[i] < stats[i+1] and stats[i] <= stats[i-1]:
                                y.append(stats[i])

                if len(y) > 0:
                        print c,dirs, y
                        fig=figure(c,dpi=10)
                        hist(y,bins=10, color = cmap2(random()))
                        grid()
                        title('Charge left before plugging in %s' % device[-1], fontsize=20)
                        xlabel('Battery Level',fontsize=15)
                        ylabel('Number of occurrences', fontsize=15)
                        pp.savefig(fig)
                        close()
                        fig.clear()
        pp.close()


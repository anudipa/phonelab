import os
from numpy import arange
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
from datetime import datetime


def chargeprof(path):
	d = os.path.join(path,'power')
        if not os.path.exists(d):
                os.makedirs(d)

#Define the names and the path of the file where graphs will be stored
        fname1 = os.path.join(d,'chargeleft.pdf')
        fname2 = os.path.join(d,'batterylevel.pdf')
	fname3 = os.path.join(d,'normalisedlevel.pdf')
	fname4 = os.path.join(d,'powerui.pdf')
        pp1 = PdfPages(fname1)
        pp2 = PdfPages(fname2)
	pp3 = PdfPages(fname3)
	pp4 = PdfPages(fname4)
        c = 0
	cmap1 = mpl.cm.autumn
	cmap2 = mpl.cm.winter
#Debug file plots the time and the correspponding battery level in a separate text file for debugging purposes
	debug = open(os.path.join(path,'check.txt'), 'w')
        for root,dirs,files in os.walk(path):
                stats = []
                timestamp = []
                filelist = []
		ui = []
		uitimestamp = []
#       print fname
#               print dirs
#               print files
                for name in files:
                        filelist.append(os.path.join(root,name))
                filelist.sort(key=os.path.getmtime)
#       name = open('/home/anudipa/logs/BatteryLogs.log','w')
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
#                                               print line + filename
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
						#debug.write('%s : %s\n' % (timestamp[-1],stats[-1]))	#debugging

#getting power ui values in order to plot transition from low to critical
					if tag.startswith('PowerUI') and data[7].startswith('updating'):
						temp = (data[11].split('='))[1]
						newdate = data[0] + '-12 ' + data[1] 
                                        	t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')

						if len(uitimestamp) == 0:
                                                         uitimestamp.append(t)
                                                         ui.append(int(temp))
                                                elif uitimestamp[-1] < t:
                                                         uitimestamp.append(t)
                                                         ui.append(int(temp))
                                                elif uitimestamp[0] > t:
                                                         uitimestamp.insert(0,t)
                                                         ui.insert(0,int(temp))
                                                else:   
                                                         for j in xrange(0,len(uitimestamp)-2):
                                                                 if uitimestamp[j] < t and uitimestamp[j+1] > t:
                                                                         uitimestamp.insert(j+1,t)
                                                                         ui.insert(j+1,int(temp))
	


                        log.close()

#*****************GRAPH PLOTTING SECTION *******************

		c = c+1		#different figure for different devices, c ----> figure number
#Getting device name from the path
		device = root.split('/')
 #Graph for plotting results from Power UI api
                if len(ui) > 0:
			fig3 = figure(c,dpi=15)
			plot(uitimestamp,ui,color=cmap2(0.7),marker='o')
			grid()
			title('Battery level from Power UI for %s' % device[-1], fontsize=20)
			xlabel('Time', fontsize=15)
			ylabel('Battery Level', fontsize=15)
			pp4.savefig(fig3)
                        close()
                        fig3.clear()



#Graph for battery level normalised for each day fo each device
		t = []
		s = []
		temp = 0
		count = 0
		debug.write('Normalised battery stats ---> %s\n' % root)
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
#					debug.write('%s : %s \n' % (t[-1],s[-1]))
			t.append(timestamp[i])
			s.append(temp)
		if len(s) > 0:
#			print s
			fig2 = figure(c,dpi=15)
			plot(t,s,color=cmap2(0.5),marker='o')
			grid()
			title('Normalised Battery Level for %s' % device[-1], fontsize=20)
			xlabel('Time', fontsize=15)
			ylabel('Battery Level', fontsize=15)
			pp3.savefig(fig2)
			fig2.clear()
			close()


#Graph for showing battery level over time for each device
                if len(stats) > 0:
                        fig1 = figure(c, dpi=15 )
                        plot(timestamp,stats,color = cmap2(0.2),marker='o')
			grid()
			xlabel('Time',fontsize=15)
			ylabel('Battery Level',fontsize=15)
                        title('Battery level for %s' % device[-1], fontsize=20)
                        pp2.savefig(fig1)
                        close()
                        fig1.clear()

#Graph for showing battery level before phone is plugged in
		debug.write('Plugged : %s\n' % root)
		y = []
                for i in xrange(1,len(stats)-2):
			if stats[i] < stats[i+1] and stats[i] <= stats[i-1]:
				y.append(stats[i])
#				debug.write('%s : %s \n' % (timestamp[i],stats[i]))

                if len(y) > 0:
                        print c,dirs, y
                        fig=figure(c,dpi=15)
                        hist(y,bins=10, color = cmap2(1))
                        grid()
                        title('Charge left before plugging in %s' % device[-1], fontsize=20)
			xlabel('Battery Level',fontsize=15)
			ylabel('Number of occurrences', fontsize=15)
                        pp1.savefig(fig)
                        close()
			fig.clear()
        pp1.close()
        pp2.close()
	pp3.close()
	pp4.close()
	debug.close()



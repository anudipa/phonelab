import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
from datetime import datetime, timedelta
from collections import defaultdict
from power import getbatterylevel, getlowlevel


def powerpred(path):
        d = os.path.join(path,'models')
        if not os.path.exists(d):
                os.makedirs(d)
        fname = os.path.join(d,'batterylevel.pdf')
        pp = PdfPages(fname)
        c = 0
	batterydata = defaultdict(int)
        for root,dirs,files in os.walk(path):
		device = root.split('/')
		c = c+1
#		fig = figure(c,dpi=20)
		timestamp = []
		stats = []
		temp = 0
		batterydata = getbatterylevel(root)
		print 'Length of returned dataset ', len(batterydata)
#		print sorted(batterydata.items())
		if len(batterydata) > 0:
			for item in sorted(batterydata.items()):
				if temp == 0:
					temp = item[0]
#					print temp
				if item[0].date() == temp.date():
#					print 'Same Day'
					timestamp.append(item[0])
					stats.append(int(item[1]))
				else:
#					print 'Plotting',stats
					fig = figure(c,dpi=20)
					c = c+1
					print len(timestamp), timestamp[0],timestamp[-1]
					plot(timestamp,stats,marker='o',color=mpl.cm.autumn(random()))
					grid()
		                        title('Battery Level for %s on %s' % (device[-1],temp.date()))
					xlabel('Time')
					ylabel('Battery Level')
					pp.savefig(fig)
					close()
					fig.clear()
					timestamp = []
					stats = []
					temp = item[0]
					timestamp.append(item[0])
					stats.append(int(item[1]))

	pp.close()



def endofday(path):
	d = os.path.join(path,'models')
        if not os.path.exists(d):
                os.makedirs(d)
        fname = os.path.join(d,'endofdaylevel.pdf')
	fname1 = os.path.join(d,'plugintime.pdf')
	fname2 = os.path.join(d,'weekendeodl.pdf')
	fname3 = os.path.join(d,'weekdayseodl.pdf')
        fname4 = os.path.join(d,'weekdaysplt.pdf')
        fname5 = os.path.join(d,'weekendsplt.pdf')
	fname6 = os.path.join(d,'weekdayllvl.pdf')
	fname7 = os.path.join(d,'weekendllvl.pdf')
        pp2 = PdfPages(fname)
	pp1 = PdfPages(fname1)
	pp3 = PdfPages(fname2)
	pp4 = PdfPages(fname3)
        pp5 = PdfPages(fname4)
        pp6 = PdfPages(fname5)
	pp7 = PdfPages(fname6)
	pp8 = PdfPages(fname7)
        c = 1

        for root,dirs,files in os.walk(path):
		total_days = 0
		batterydata = defaultdict(int)
		lowlvldata = defaultdict(int) 
                device = root.split('/')
                c = c+1
		timestamp = []
		levels = []
		timelist = []
		t = []
		print 'Now Checking ', device[-1], '-->',root
		if len(device[-1]) > 1:
			batterydata = getbatterylevel(root)
			lowlvldata = getlowlevel(root)
		temp = 0
		last = 0
		last_date = 0
		flag = 0

		ui = []
		m = []
		n = []
#Working with low level data. finding out when device's battery charge falls into low level
		if len(lowlvldata) > 0:
#			print 'Low level data \n', lowlvldata, '\n***********************\n'
			for item in sorted(lowlvldata.items()):
				if temp == 0:
					temp = item[0]
				if item[1] == 14:
					if len(t) > 0 and item[0].hour - t[-1].hour > 3:
						ui.append(item[0].hour)
						t.append(item[0])
					elif len(t) == 0:
						ui.append(item[0].hour)
                                       	 	t.append(item[0])
			for i in xrange(0,len(t)):
				print t[i].date(), 'is ',t[i].weekday(),ui[i]
				if t[i].weekday() < 5:
					m.append(ui[i])
				else:
					n.append(ui[i])
#			print m
#			print n
			if len(m) > 0:
				print 'For Weekdays',len(m), m
	                        fig5 = figure(c,dpi=10)
        	                c = c+1
				hist(m,color=mpl.cm.hsv(random()))
				grid()
				title('When %s hits low battery level on Weekdays' % device[-1])
				xlabel('Time in hours')
				ylabel('Number of occurrences')
				pp7.savefig(fig5)
				close()
				fig5.clear()
			if len(n) > 0:
				print 'For Weekends', len(n), n
	                        fig6 = figure(c,dpi=10)
        	                c = c+1
                	        hist(n,color=mpl.cm.hsv(random()))
				grid()
	                        title('When %s hits low battery level on Weekends' % device[-1])
        	                xlabel('Time in hours')
                	        ylabel('Number of occurrences')
                        	pp8.savefig(fig6)
	                        close()
        	                fig6.clear()
#Working with battery levels at the end of the day and also to find when phone is charging
		t = []
		temp = 0
		if len(batterydata) > 0:
			fig = figure(c,dpi=30)
			for item in sorted(batterydata.items()):
                                if temp == 0:
                                        temp = item[0]
					last = item[1]
					last_date = item[0]
					total_days += 1
#                                        print 'Debug',last_date
                                if item[0].date() == temp.date():
#                                       print 'Same Day'
					if flag == 0:
						if item[1] < last:
							flag = 1
						last = item[1]
						last_date = item[0]
					else:
#						if item[1] < last:
						timelist.append(last_date.hour)
						t.append(last_date)
						flag = 0
					last = item[1]
                                        last_date = item[0]	

                                else:
#                                       print 'Plotting',stats
					total_days += 1
					if not last_date == 0:
						levels.append(last)
						timestamp.append(last_date)
					temp = item[0]
                                last = item[1]
                                last_date = item[0]        

			print '\nTotal number of days = ',total_days

#			print 'Time for charging',timelist
			if len(timelist) > 0:
				fig1 = figure(c,dpi=10)
				c += 1
				hist(timelist,bins=20,color=mpl.cm.hsv(random()))
				grid()
				title('Time of the day when %s is charged' % device[-1])
				xlabel('Time')
				ylabel('Number of occurrences')
				pp1.savefig(fig1)
				close()
				fig1.clear()
			a = []
			b = []
			for i in xrange(0,len(t)):
				if t[i].weekday() < 5:
					a.append(t[i].hour)
				else:
					b.append(t[i].hour)

#			print '\n\n Time for charging on weekdays',a
			if len(a) > 0:
				fig11 = figure(c,dpi=10)
				c += 1
				hist(a,bins=20,color=mpl.cm.hsv(random()))
                        	grid()
	                        title('Time of the day when %s is charged(Weekdays)' % device[-1])
        	                xlabel('Time')
                	        ylabel('Number of occurrences')
                        	pp5.savefig(fig11)
	                        close()
				fig11.clear()
			if len(b) > 0:
				fig12 = figure(c,dpi=10)
				c += 1
				hist(b,bins=20,color=mpl.cm.hsv(random()))
                        	grid()
	                        title('Time of the day when %s is charged(Weekends)' % device[-1])
        	                xlabel('Time')
                	        ylabel('Number of occurrences')
                        	pp6.savefig(fig12)
	                        close()
				fig12.clear()

#			print 'Charge left at end of day',levels,timestamp
			if len(levels) > 0:
				fig2 = figure(c,dpi=10)
				c += 1
                	        hist(levels,bins=20,color=mpl.cm.hsv(random()))
                        	grid()
	                        title('Charge at the end of day for %s' % device[-1])
        	                xlabel('Battery Level')
                	        ylabel('Number of occurrences')
                        	pp2.savefig(fig2)
	                        close()
        	                fig2.clear()
			x = []
			y = []
#			print timestamp
			for i in xrange(0,len(timestamp)):
				if timestamp[i].weekday() < 5:
					x.append(levels[i])
				else:
					y.append(levels[i])
			if len(y) > 0:
				fig3 = figure(c,dpi=10)
				c += 1
				hist(y,bins=20,color=mpl.cm.hsv(random()))
				grid()
				title('Charge at end of weekends for %s' % device[-1])
				xlabel('Battery Level')
				ylabel('Number of occurrences')
				pp3.savefig(fig3)
				close()
				fig3.clear()
			if len(x) > 0:
	                        fig4 = figure(c,dpi=10)
				c += 1
                	        hist(x,bins=20,color=mpl.cm.hsv(random()))
                        	grid()
	                        title('Charge at end of weekdays for %s' % device[-1])
        	                xlabel('Battery Level')
                	        ylabel('Number of occurrences')
                        	pp4.savefig(fig4)
	                        close()
        	                fig4.clear()

#			print '\n**************\nTotal number of days = ',total_days
#		print'\n*******************\n'
				
	pp1.close()		
	pp2.close()
	pp3.close()
	pp4.close()
	pp5.close()
	pp6.close()
	pp7.close()
	pp8.close()




def connectivity(path):
        d = os.path.join(path,'models')
        if not os.path.exists(d):
                os.makedirs(d)
        fname = os.path.join(d,'wifiQA.pdf')
        pp = PdfPages(fname)
#Dictionaries to store information about bssid
	ssid_dict = defaultdict(list)		#holds all bssid-s encountered under each ssid
	bssid_dict = defaultdict(list)		#holds no. of good and bad connxns for each bssid
#details about all bad connxns: device -> { timestamp -> { bssid, signal} }
  	device_dict = defaultdict(lambda : defaultdict(list))

#Iterating through the path given to parse all files and collect required data
	for root,dirs,files in os.walk(path):
		filelist = []
#Assumption: Directory name = Device name
		device = root.split('/')
		devname = device[-1]
                for name in files:
                        filelist.append(os.path.join(root,name))
                filelist.sort(key=os.path.getmtime)
#The variables to store data required for intermediary comparison
		t_ssid = '0'
		t_bssid = '0'
		t_signal = 0
		t_time = datetime.now() 
#Debugging variable
		flag = 0

                for filename in filelist:
                        try:
                                log = open(filename,'r')
                        except IOError:
                                print 'File doesnot exit'
                                break
                        for line in log:
                                data = line.split()
                                n = len(data)
                                if n < 8 or data[0].startswith('01') or data[0].startswith('12'):
#                                               print line + filename
                                        pass
                                else:
                                        tag = data[5]
					temp = data[7]
                                        newdate = data[0] + '-12 ' + data[1]
					try:
                                        	t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
					except:
						print 'Line doesnot start with timestamp'
                                        if tag.startswith('wpa_supplicant') and data[6].startswith('wlan') and data[7].startswith('Trying'):
						t_bssid = data[11]
						t_ = data[12].split('=')
						t_ssid = t_[-1]
	#					print 'Current ',t_bssid, t_ssid
#						t_time = t
						flag = 0
					elif tag.startswith('wpa_supplicant') and data[6].startswith('wlan') and data[-1].startswith('out') and data[-2].startswith('timed'):
						t_ssid = '0'
						t_bssid = '0'
						t_time = datetime.now()
					elif tag.startswith('wpa_supplicant') and data[6].startswith('wlan') and data[7].startswith('CTRL-EVENT-CONNECTED') and data[11].startswith(t_bssid):
						print 'Connection Established ', t_bssid, t_ssid
						try:
							ssid_dict[t_ssid].index(t_bssid)
						except:
							ssid_dict[t_ssid].append(t_bssid)
#Assumption: Every connection is a good connection unless proven otherwise
						if len(bssid_dict[t_bssid]) == 2:
							bssid_dict[t_bssid][0] += 1
						else:
							bssid_dict[t_bssid].append(1)
							bssid_dict[t_bssid].append(0)
						t_time = t
						flag = 1
					elif flag == 1 and tag.startswith('wpa_supplicant') and data[6].startswith('wlan') and data[7].startswith('CTRL-EVENT-DISCONNECTED') and t - t_time < timedelta(minutes=10) and data[8].endswith(t_bssid):
#If connection break within first 10 mins, it is a bad connection
						print 'Bad Connection'
						device_dict[devname][t].append(t_bssid)
						device_dict[devname][t].append(t_signal)
						try:
							bssid_dict[t_bssid][0] -= 1
							bssid_dict[t_bssid][1] += 1
						except:
							print 'Error!! Disconnected before connecting',len(bssid_dict[t_bssid]), flag
							bssid_dict[t_bssid].append(0)
                                                        bssid_dict[t_bssid].append(1)
#Flushing all reference variables
						t_bssid = '0'
						t_ssid = '0'
						t_time = datetime.now()
						flag = 0
					elif tag.startswith('PhoneLab-StatusMonitorSignal') and data[6].startswith('Signal_Strength'):
						t_signal = int(data[7])
						
			log.close()
	x = []
	y = []
#	for items in bssid_dict:
#		mylist = bssid_dict[items]
#		print mylist, '------>',items
#		if len(mylist) == 2:
#			x.append(mylist[0])
#			y.append(mylist[1])
#	bar(x,y,color = mpl.cm.hsv(random()))
	
	print ssid_dict['blue']
	c=0

	for item1 in ssid_dict:
		bssid_list = ssid_dict[item1]
		print item1,ssid_dict[item1]
		for i in xrange(0,len(bssid_list)):
			item2 = bssid_list[i]
			mylist = bssid_dict[item2]
			if len(mylist) == 2:
				x.append(mylist[0])
				y.append(mylist[1])
				
		if len(x) > 0:
			fig = figure(c,dpi=10)
			n = range(len(x))
			bar(n,x,color = mpl.cm.hsv(random()))
			bar(n,y,color = mpl.cm.hsv(random()))
			legend(["Good","Bad"])
			title('Quality of connection offered by %s(#%d)' % (item1,len(x)))
			xlabel('Different BSSIDs', fontsize=15)
			ylabel('Number of connections', fontsize=15)
			pp.savefig(fig)
			close()
			c = c+1
		x = []
		y = []
	pp.close()

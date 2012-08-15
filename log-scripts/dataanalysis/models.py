import os
from numpy import arange
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
		print 'Now Checking ', device[-1]
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
			print 'Low level data \n', lowlvldata, '\n***********************\n'
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
				if t[i].weekday < 5:
					m.append(ui[i])
				else:
					n.append(ui[i])
#			print m
#			print n
			if len(m) > 0:
				print 'For Weekdays',len(m)
	                        fig5 = figure(c,dpi=10)
        	                c = c+1
				hist(m,bins=20,color=mpl.cm.hsv(random()))
				grid()
				title('When %s hits low battery level on Weekdays' % device[-1])
				xlabel('Time in hours')
				ylabel('Number of occurrences')
				pp7.savefig(fig5)
				close()
				fig5.clear()
			if len(n) > 0:
				print 'For Weekends', len(n)
	                        fig6 = figure(c,dpi=10)
        	                c = c+1
                	        hist(n,bins=20,color=mpl.cm.hsv(random()))
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
                                        print 'Debug',last_date
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


			print '\n**************\nTotal number of days = ',total_days
#			print 'Time for charging',timelist
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

				
	pp1.close()		
	pp2.close()
	pp3.close()
	pp4.close()
	pp5.close()
	pp6.close()
	pp7.close()
	pp8.close()

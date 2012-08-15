import os
import numpy as np
import matplotlib as mpl
from matplotlib.dates import WeekdayLocator, DateFormatter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
from pylab import *
from datetime import datetime, timedelta
from collections import defaultdict
from wifi import signaldata
from gps import gpsdata

def guessloc(path, bssid):
	xy = [[0.0,-1.0],[0.0,-180.0],[90.0,-180.0],[90.0,-1.0]]
	spotted = defaultdict(list)
	for root,dirs, files in os.walk(path):
                filelist = []
                for name in files:
                        filelist.append(os.path.join(root,name))
                filelist.sort(key=os.path.getmtime)
#		signaldata = signaldata(root)
		#gpsdict = gpsdata(root)
		signaldict = signaldata(root)
#		print signaldict
		gpsdict = gpsdata(root)
		flag = 0
		device = root.split('/')
		print 'Now Checking ', device[-1]
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
                                        continue
                                else:
                                        tag = data[5]
					if data[5].startswith('PhoneLab-WiFiReceiver') and data[8].startswith('BSSID'):
						if data[9] == bssid:
#							flag  = 1
#							print 'Matched BSSID ',data[9],'Flag: ', flag
							newdate = data[0] + '-12 ' + data[1]
							t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
							flag = t
#							print 'set the flag',flag

					elif not flag== 0 and data[5].startswith('PhoneLab-WiFiReceiver') and data[8].startswith('disconnected'):
#						print 'Flag is Reset !!'
						
						newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
#						print 'Reset flag ', t
						for item1 in signaldict:
#							print item1,' > ', flag, ':',(item1 > flag)
#							if item1 < t and (item1-flag) < (t - flag):
							if item1 < t and item1 > flag:
								sig = signaldict[item1]
#								print item1, ':', sig
								if int(sig) > -96:
									for item in gpsdict:
										if item.minute-item1.minute < 2 and item.minute-item1.minute > -2:
											loc = gpsdict[item]
#											print loc
											lat = loc[0]
											lon = loc[1]
											spotted[device[-1]].append(float(lat))
											spotted[device[-1]].append(float(lon))
											
							
						flag  = 0

#					elif flag == 1 and data[5].startswith('PhoneLab-StatusMonitorSignal') and data[6].startswith('Signal_Strength'): 
#						newdate = data[0] + '-12 ' + data[1]
#                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
#						print 'Signal Strength: ', data[7]
#						if data[7] > -86:
#							gpsdict = gpsdata(filename)
#							dict_ = defaultdict(float)
#							for item in gpsdict:
#								if item.minute-t.minute < 2 and item.minute-t.minute > -1:
#									loc = gpsdict[item]
#									lat = loc[0]
#									lon = loc[1]
#									spotted[device[-1]].append(float(lat))
#									spotted[device[-1]].append(float(lon))
					
									
			log.close()
		
#	print spotted
	devicelist = []
	print xy
	for item in spotted:
                loclist = spotted[item]
		devicelist.append(item)
		maxlat = float(loclist[0])
		minlat = float(loclist[0])
		maxlon = float(loclist[1])
		minlon = float(loclist[1])
		for i in xrange(0,len(loclist),2):
			if maxlat < loclist[i]:
				maxlat = loclist[i]
			elif minlat > loclist[i]:
				minlat = loclist[i]
		for i in xrange(1,len(loclist),2):
			if maxlon < loclist[i]:
				maxlon = loclist[i]
			elif minlon > loclist[i]:
				minlon = loclist[i]
		print maxlat, minlat, maxlon, minlon
		if xy[0][0] < maxlat:
			xy[0][0] = maxlat
			xy[1][0] = maxlat
		if xy[2][0] > minlat:
			xy[2][0] = minlat
			xy[3][0] = minlat
		if xy[0][1] > minlon:
			xy[0][1] = minlon
			xy[3][1] = minlon
		if xy[1][1] < maxlon:
			xy[1][1] = maxlon 
			xy[2][1] = maxlon
	print '\nThe devices came across given bssid\n',devicelist,'\n\n'
	print 'Guessing the 4 corners of the square within which ',bssid,' probably exists--> upper left:',xy[0][0],xy[0][1],' upper right:',xy[1][0],xy[1][1], ' lower right:',xy[2][0],xy[2][1],' lower left:',xy[3][0],xy[3][1]

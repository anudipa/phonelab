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
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import gps
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")




def gps2xml(path):
	gpsdict = defaultdict(list)
	generated_on = str(datetime.now())
	root = Element('root')
	comment = Comment('Generated for tool analysis')
	root.append(comment)
#	body = SubElement(root,'body')
	
	for roots,dirs,files in os.walk(path):
		device = roots.split('/')
		if len(device[-1]) > 8:
			gpsdict = gps.gpsdata(roots)
			node = SubElement(root,'device',{'id':device[-1]})
			if len(gpsdict) > 0 :
				temp = 0
				current_group = None
				for item in sorted(gpsdict.items()):
#					print item[1]
					if temp == 0 or not temp == item[0].date():
						temp = item[0].date()
						date  = SubElement(node,'date',{'value':str(temp)})
					current_group= SubElement(date,'details',{'timestamp':str(item[0].time())})
					child1 = SubElement(current_group,'latitude')
					child1.text = item[1][0]
					child2 = SubElement(current_group,'longitude')
					child2.text = item[1][1]

		
	d = os.path.join(path,'xml')
        if not os.path.exists(d):
                os.makedirs(d)
	fname = os.path.join(d,'gps.xml')
	f = open(fname,'w')
	f.write(prettify(root))
	f.close()


def bssid2xml(path):
	bssid_dict = defaultdict(list)
	device_dict = defaultdict(lambda:defaultdict(list))
	bssid_dev = defaultdict(list)

#Part 1:	a.populate bssid_dict with all bssid-s encountered along with associated bad and good connections	b.populate bssid_dev with bssid as key and devices that seen it as values
	for root,dirs,files in os.walk(path):
		filelist = []
                for name in files:
                        filelist.append(os.path.join(root,name))
                filelist.sort(key=os.path.getmtime)
                t_time = datetime.now()
                flag = 0
		t_ssid = '0'
		t_bssid = '0'
		t_signal = '0'
		t_loc = ['0' , '0']
		device = root.split('/')
		devname = device[-1]

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
                                        try:
						newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
                                        except:
                                                print 'Line doesnt start with timestamp'
						continue
					
                                        if tag.startswith('wpa_supplicant') and data[6].startswith('wlan') and data[7].startswith('Trying'):
                                                t_bssid = data[11]
#                                               t_time = t
                                                flag = 0
					elif tag.startswith('wpa_supplicant') and data[6].startswith('wlan') and data[-1].startswith('out') and data[-2].startswith('timed'):
                                                t_ssid = '0'
                                                t_bssid = '0'
                                                t_time = datetime.now()
                                        elif tag.startswith('wpa_supplicant') and data[6].startswith('wlan') and data[7].startswith('CTRL-EVENT-CONNECTED') and data[11].startswith(t_bssid):
                                                print 'Connection Established ', t_bssid, t_ssid
#Assumption: Every connection is a good connection unless proven otherwise
                                                if len(bssid_dict[t_bssid]) == 2:
                                                        bssid_dict[t_bssid][0] += 1
                                                else:
                                                        bssid_dict[t_bssid].append(1)
                                                        bssid_dict[t_bssid].append(0)
                                                t_time = t
                                                flag = 1
					elif flag == 1 and tag.startswith('wpa_supplicant') and data[6].startswith('wlan') and data[7].startswith('CTRL-EVENT-DISCONNECTED') and t - t_time < timedelta(minutes=5) and data[8].endswith(t_bssid) and not t_signal == '0':
#If connection break within first 5 mins, it is a bad connection
						print 'Bad Connection'
						device_dict[devname][t].append(t_bssid)
                                                device_dict[devname][t].append(t_signal)
                                                device_dict[devname][t].append(t_loc[0])
                                                device_dict[devname][t].append(t_loc[1])
  
                                                try:
                                                        bssid_dict[t_bssid][0] -= 1
                                                        bssid_dict[t_bssid][1] += 1
                                                except:
                                                        print 'Error!! Disconnected before connecting',len(bssid_dict[t_bssid]), flag
                                                        bssid_dict[t_bssid].append(0)
                                                        bssid_dict[t_bssid].append(1)
						try:
							bssid_dev[t_bssid].index(devname)
						except:
							bssid_dev[t_bssid].append(devname)


#Flushing all reference variables
                                                t_bssid = '0'
                                                t_time = datetime.now()
                                                flag = 0
					elif tag.startswith('PhoneLab-StatusMonitorSignal') and data[6].startswith('Signal_Strength'):
                                                t_signal = data[7]
                                        elif tag.startswith('PhoneLab-StatusMonitorLocation') and data[6].startswith('Location_Latitude'):
                                                t_loc[0] = data[7]
                                                t_loc[1] = data[9]


			log.close()
#Part 2: get signal-location pair from all devices which have seen a particular bssid
	root = Element('root')
        comment = Comment('Generated for tool analysis')
        root.append(comment)

	for bssid in bssid_dict:
		if bssid_dict[bssid][1] > 50 and not bssid == '0':
		 	list_ = bssid_dev[bssid]
			node = SubElement(root,'bssid',{'val':bssid})
			temp = 0
			current_group = None
			print bssid, '------->', bssid_dict[bssid]
			print bssid_dev[bssid]
			for i in xrange(1,len(list_)):
				dev = SubElement(node,'device',{'id':str(list_[i])})
				print list_[i]
				for item in sorted(device_dict[list_[i]].items()):
					if item[1][0] == bssid:
						current_group = SubElement(dev,'details',{'timestamp':str(item[0].time())})
						child1 = SubElement(current_group,'signal')
						child1.text = str(item[1][1])
						child2 = SubElement(current_group,'latitude')
	                                        child2.text = item[1][2]
        	                                child3 = SubElement(current_group,'longitude')
                	                        child3.text = item[1][3]
	d = os.path.join(path,'xml')
        if not os.path.exists(d):
                os.makedirs(d)
        fname = os.path.join(d,'cqa.xml')
        f = open(fname,'w')
        f.write(prettify(root))
        f.close()


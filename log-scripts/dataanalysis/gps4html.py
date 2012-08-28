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

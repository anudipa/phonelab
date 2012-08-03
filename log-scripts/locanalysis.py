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


def analyse(path):
#Define the names and the path of the file where graphs will be stored
#        fname1 = os.path.join(path,'location.pdf')
	
#	pp1 = PdfPages(fname1)
	cmap1 = mpl.cm.autumn	

#Debug file has a debugging purposes
        debug = open(os.path.join(path,'wificheck.txt'), 'w')
        for root,dirs,files in os.walk(path):
		timestamp = []
		lat = []
		lon = []
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
                                        if tag.startswith('PhoneLab-StatusMonitorLocation') and data[6].startswith('Location_Latitude'):
						latitude = data[7]
						longitude = data[9]
                                                newdate = data[0] + '-12 ' + data[1]
                                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
                                                if len(timestamp) == 0:
                                                        timestamp.append(t)
                                                        lat.append(float(latitude))
							lon.append(float(longitude))
                                                elif timestamp[-1] < t:
                                                        timestamp.append(t)
                                                        lat.append(float(latitude))
							lon.append(float(longitude))
                                                elif timestamp[0] > t:
                                                        timestamp.insert(0,t)
                                                        lat.insert(0,float(latitude))
							lon.append(float(longitude))
                                                else:
                                                        for j in xrange(0,len(timestamp)-2):
                                                                if timestamp[j] < t and timestamp[j+1] > t:
                                                                        timestamp.insert(j+1,t)
                                                                        lat.insert(j+1,float(latitude))
									lon.append(float(longitude))
#		print 'Latitude',lat
		
#*************************Start plotting the locations on map. (Fingers Crossed)************************
#Discard consecutive similar locations

		newlat = []
		newlon = []
		newtime = []
		if len(lat) > 0:
	                maxlat = max(lat)
	                minlat = min(lat)
        	        maxlon = max(lon)
                	minlon = min(lon)
			print maxlat, minlat, maxlon, minlon
			
			for i in xrange(0,len(lat)-2):
				if lat[i] != lat[i+1] and lon[i] != lon[i+1]:
					newlat.append(lat[i])
					newlon.append(lon[i])
					newtime.append(timestamp[i].date())

#		print newlat, newlon
#			fig = figure(c,dpi=20)
			device = root.split('/')
#			M = Basemap(projection='lcc', llcrnrlat=minlat-2, llcrnrlon=maxlon+2, urcrnrlat=maxlat+2, urcrnrlon=minlon-2, lat_0 = (minlat+maxlat)/2, lon_0 = (minlon+maxlon)/2,resolution = 'f')
			nx = []
			ny = []
#			M = Basemap(projection='cyl', lat_0 = (minlat+maxlat)/2, lon_0 = (minlon+maxlon)/2,resolution = 'f')
#			nx, ny = M(newlon,newlat)
#			nlati = np.linspace(minlat, maxlat, len(nx))
#			nloni = np.linspace(maxlon,minlon,len(ny))
#			ntime = griddata(newlon,newlat,newtime,nloni,nlati)
#			M.contourf(nx,ny,ntime)
#			M.transform_scalar(newtime,lon,lat,nx,ny)
#			M.bluemarble()
#			M.imshow()
#			M.bluemarble()
#			x,y = M(newlon,newlat)
#			M.drawlsmask()
#			M.fillcontinents(color='coral')
#			M.plot(nx,ny,'*')
#			legend(newtime)
			print device[-1], len(newlat), len(newlon)
#			title('GPS locations for %s' % device[-1])
#			pp1.savefig(fig)
#			close()

			thislon = []
			thislat = []
			thisleg = []
			temp = newtime[0]
			namestr = 'location'+device[-1]+'.pdf'
			fname1 = os.path.join(path,namestr)
		        pp1 = PdfPages(fname1)
			c = 0
			for t in xrange(0,len(newtime)-1):
				if temp!=newtime[t] or t == len(newtime)-1:
					fig = figure(c,dpi=20)
					ax = fig.add_axes([0.1,0.1,0.8,0.8])
					minlat = min(thislat)
					maxlat = max(thislat)
					minlon = min(thislon)
					maxlon = max(thislon)
					M = Basemap(projection='lcc', llcrnrlat=minlat-5, llcrnrlon=minlon-10, urcrnrlat=maxlat+5, urcrnrlon=maxlon+10, lat_0=(maxlat+minlat)/2, lon_0 =(maxlon+minlon)/2 ,area_thresh=0.5,resolution = 'f',ax=ax)

					M.drawlsmask()
					M.fillcontinents(color='coral')
					parallels = np.arange(minlat-5,maxlat+5,5.)
					M.drawparallels(parallels)
#					meridians = np.arange(minlon-5,maxlon+5,5.)
#					M.drawmeridians(meridians)
					x,y=M(thislon,thislat)
					M.plot(x,y,'--*')
#					legend(thisleg)
					title('GPS Location for %s on %s(count=%d)' % (device[-1],temp.strftime('%B %d, %Y'),len(thislon)))
					temp = newtime[t]
					thislat = []
					thislon = []
					thisleg = []
					pp1.savefig(fig)
					close()
					c = c+1
				thislat.append(newlat[t])
                                thislon.append(newlon[t])
				string = str(lat[t]) + ' ' + str(lon[t])
				thisleg.append(string)
			pp1.close()
#	c += 1
#	pp1.close()



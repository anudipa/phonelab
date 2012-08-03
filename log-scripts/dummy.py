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
						print latitude, longitude
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
#               print 'Latitude',lat

#*************************Start plotting the locations on map. (Fingers Crossed)************************
#Discard consecutive similar locations

                newlat = []
                newlon = []
                newtime = []
		print len(lat), len(lon)
		if len(lat) > 1:
			for i in xrange(0,len(lat)-2):
				if lat[i] != lat[i+1] and lon[i] != lon[i+1]:
					newlat.append(lat[i])
        	                        newlon.append(lon[i])
                	                newtime.append(timestamp[i].date())

#               print newlat, newlon
#                       fig = figure(c,dpi=20)
                device = root.split('/')
		if len(newlat) > 0:
                        maxlat = max(newlat)
                        minlat = min(newlat)
                        maxlon = max(newlon)
                        minlon = min(newlon)
                        print maxlat, minlat, maxlon, minlon

	
		topoin = newtime
		lons = newlon
		lats = newlat
# shift data so lons go from -180 to 180 instead of 20 to 380.
#		topoin,lons = shiftgrid(180.,topoin,lons,start=False)

# plot topography/bathymetry as an image.

# create the figure and axes instances.
		fig = plt.figure()
		ax = fig.add_axes([0.1,0.1,0.8,0.8])
# setup of basemap ('lcc' = lambert conformal conic).
# use major and minor sphere radii from WGS84 ellipsoid.
		m = Basemap(llcrnrlon=minlat-1,llcrnrlat=maxlon+1,urcrnrlon=minlon-1,urcrnrlat=maxlat+1,\
        	    rsphere=(6378137.00,6356752.3142),\
	            resolution='f',projection='lcc',\
        	    lat_0= (minlat+maxlat)/2,lon_0= (minlat+maxlat)/2,ax=ax)
# transform to nx x ny regularly spaced 5km native projection grid
		nx = int((m.xmax-m.xmin)/5.)+1; ny = int((m.ymax-m.ymin)/5.)+1
		topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
# plot image over map with imshow.
		im = m.imshow(topodat,cm.GMT_haxby)
# draw coastlines and political boundaries.
		m.drawcoastlines()
		m.drawcountries()
		m.drawstates()
# draw parallels and meridians.
# label on left and bottom of map.
		parallels = np.arange(0.,80,20.)
		m.drawparallels(parallels,labels=[1,0,0,1])
		meridians = np.arange(10.,360.,30.)
		m.drawmeridians(meridians,labels=[1,0,0,1])
# add colorbar
		cb = m.colorbar(im,"right", size="5%", pad='2%')
		ax.set_title('ETOPO5 Topography - Lambert Conformal Conic')
		plt.show()


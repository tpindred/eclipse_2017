from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

gpx_file = "eclipse_data_2017.gpx"

# Take in the .gpx eclipse file and return a dict containing lists of lon & lat lists for each path. 
def getGpsPoints(gpxfile):  
    tree = ET.parse(gpxfile)
    namespace = {'ns': 'http://www.topografix.com/GPX/1/1'} # Namespace to make findall searches less verbose
    data = {}
    tracks = tree.findall("./ns:trk", namespace)
    for track in tracks:
        lons = []
        lats = []
        name = track.findall('./ns:name', namespace)
        name = name[0].text
        trackpoints = track.findall('.//ns:trkpt', namespace)
        for trackpoint in trackpoints:
            lon = trackpoint.attrib['lon']
            lat = trackpoint.attrib['lat']
            lons.append(float(lon))
            lats.append(float(lat))
        data[name] = [lons,lats]
    return data

# Take a dict of gps data and plot on a mercator projection map of the US
def plotGpsData(gpsdata):
    m = Basemap(llcrnrlon=-127, llcrnrlat=25, urcrnrlon=-67, urcrnrlat=50, lat_ts=45, resolution='l', projection='merc', lat_0=45, lon_0=-90)
    m.drawmapboundary(fill_color='aqua')
    m.drawcoastlines()
    m.fillcontinents(color='green', lake_color='aqua')
    m.drawstates()
    m.drawcountries()
    for name, points in gpsdata.items():
        x1, y1 = m(points[0], points[1])
        m.scatter(x1, y1, c='k', zorder=10, label=name) # zorder makes the points visible above the map background
    plt.title("2017 Solar Eclipse GPS Data")
    plt.show()

def main():
    gpsdata = getGpsPoints(gpx_file)
    plotGpsData(gpsdata)
    
if __name__ == "__main__":
    main()


from math import cos, asin, sqrt, pi
import googlemaps
import APIKey
#returns elevation based on a point using elevation api, in km
def getElevation(lat,lon):
    gmaps = googlemaps.Client(key=APIKey.googleMapsAPI)
    returndata = gmaps.elevation((lat, lon))[0]['elevation']/1000
    #print(returndata)
    return returndata

#returns distance based on two points and elevation difference(km)
def distance(point1, point2, elevationdif): 
    lat1, lon1 = point1
    lat2, lon2 = point2
    r = 6371 # km
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    dist2d = 2 * r * asin(sqrt(a))
    return sqrt(dist2d**2 + elevationdif**2)

#returns surrounding 4 points and itself based on start point and end point for quadratic surface method for hill slope
def surrounding(start, end): 
    surroundpoint = [] 
    startpointlat, startpointlon = start
    dif = {'lat': end[0]-startpointlat, 'lon': end[1]-startpointlon}
    surroundpoint.append((startpointlat+dif['lat'], startpointlon+dif['lon']))
    surroundpoint.append((startpointlat-dif['lat'], startpointlon-dif['lon']))
    surroundpoint.append((startpointlat+dif['lon'], startpointlon-dif['lat']))
    surroundpoint.append((startpointlat-dif['lon'], startpointlon+dif['lat']))
    return surroundpoint

# returns hill slope by degrees using start, end and surrounding points
def quadraticSurfaceMethod(start, end):
    surroundingpts = surrounding(start, end)
    elevations = []
    for lat, lon in surroundingpts:
        elevations.append(getElevation(lat, lon))
    celRes = distance(start, end, 0)
    g = (elevations[2]-elevations[3])/(2*celRes)
    h = (elevations[0]-elevations[1])/(2*celRes)
    return 100*sqrt(g**2 + h**2)

def test():
    return getElevation(0,0)

import projectqsm as qsm
import numpy as np
import math
from lxml import etree
from importlib import reload
qsm = reload(qsm)

#returns array of lat and lon points of each track point from gpx xml
def extractPoints(xml):
    namespace = xml.xpath('namespace-uri(/*)')
    find = './/{'+namespace+'}trkseg'
    print(find)
    trail = xml.findall(find)
    returnarr = []
    if len(trail) != 0:
        trail = trail[0]
        for item in trail.iter('{'+namespace+'}trkpt'):
            returnarr.append((float(item.attrib['lat']),float(item.attrib['lon'])))
        return returnarr
    else:
        raise Exception("trail not found")
        return None

#'{'+namespace+'}trkpt'

#calculates average time (hrs) to hike through a trail, using a xml element as input 
def calcAvgHikingTime(xml):
    trailpoints = extractPoints(xml)
    time = 0 #hrs
    additionalData = [-1,0,10000000,0,0]
    for index in range(0, int(len(trailpoints)/1)-2):
        start = trailpoints[index]
        end = trailpoints[index+1]
        hillslope = qsm.quadraticSurfaceMethod(start, end)
        startElevation = qsm.getElevation(start[0], start[1])
        endElevation = qsm.getElevation(end[0], end[1])
        extractAdditionalInfo(additionalData, startElevation, endElevation, start, end)
        walkingslope = np.rad2deg(np.arctan2(endElevation-startElevation, qsm.distance(start,end,0)))
        intercept = 1.536
        avgSpeed = math.exp(intercept - 0.00965*walkingslope - 0.00187*(walkingslope**2) - 0.00731*hillslope) # km/h
#         print(start)
#         print(end)
#         print('distance:' + str(qsm.distance(start,end,(endElevation-startElevation))) + ' speed: ' + str(avgSpeed) + ' time: ' + str(qsm.distance(start,end,(endElevation-startElevation))/avgSpeed))
        time = time + qsm.distance(start,end,(endElevation-startElevation))/avgSpeed
    return (time, additionalData)

# additionalarr: [maxElevation, uphill, minElevation, downhill, length]
def extractAdditionalInfo(additionalarr, startElevation, endElevation, start, end):
        additionalarr[0] = (additionalarr[0], startElevation) [additionalarr[0] < startElevation]
        additionalarr[0] = (additionalarr[0], endElevation) [additionalarr[0] < endElevation]
        additionalarr[2] = (additionalarr[2], startElevation) [startElevation < additionalarr[2]]
        additionalarr[2] = (additionalarr[2], endElevation) [endElevation < additionalarr[2]]
        if (endElevation-startElevation > 0):
            additionalarr[1] = additionalarr[1] + (endElevation-startElevation)
        else:
            additionalarr[3] = additionalarr[3] - (endElevation-startElevation)
        additionalarr[4] = additionalarr[4] + qsm.distance(start,end,(endElevation-startElevation))
        
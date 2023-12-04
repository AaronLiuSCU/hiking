import os
import re
import errno
from pathlib import Path
import pandas as pd
from lxml import etree

#removes encoding attribute. unfortunately python does not allow modifying strings in place
def removeEncoding(xmlString):
    remove = re.search("\s+encoding\s*\=\".+\"", xmlString)
    if(remove == None):
        return xmlString
    remove = remove.group()
    return xmlString.replace(remove, "")
def test():
    print('a')

# Returns a xml root from gpx file if fileInput is inputted, or xml string containing a piece of data from .csv dataset
def returnGPXData(fileInput):
    path = '';
    try:
        path = os.path.abspath(os.path.dirname(os.getcwd()))
    except:
        raise Exception("file directory access denied/doesn't exist")
    root = None
    if type(fileInput) == int:
        if fileInput < 12000 and fileInput >= 0:
            path = os.path.join(path, "data/gpx-tracks-from-hikr.org.csv")
            df = pd.read_csv(path)
            parser = etree.XMLParser(recover=True)
            gpxString = removeEncoding(df.gpx[fileInput])
            return etree.fromstring(gpxString, parser)
        else:
            raise Exception("index for gpx file out of range")
    else:
        path = os.path.join(path, "inputData/"+fileInput)
        try:
            return etree.parse(path).getroot()
        except:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), fileInput)
    # df = df.drop(['_id', 'user', 'start_time', 'end_time', 'max_elevation','max_speed', 'url'], axis = 1)
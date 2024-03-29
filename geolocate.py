#specify image directory
#this program reads location data and writes javascript file of array of [img src, lat, lng] for each image



import glob
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
 
def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
 
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
 
    return exif_data
 
def _get_if_exist(data, key):
    if key in data:
        return data[key]
		
    return None
	
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)
 
    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)
 
    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)
 
    return d + (m / 60.0) + (s / 3600.0)
 
def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None
 
    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]
 
        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')
 
        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat
 
            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon
 
    return lat, lon


#directory = "\\home\\gkrathwohl\\public_html\\middGuessr\\midd\\"

directory = os.getcwd()


images = glob.glob(os.path.join(directory,"midd","*.JPG"))

print directory

f = open('imgs.js','w')
f.write('a=[') # python will convert \n to os.linesep
  
	

def publicHtml(path):
	return "'." + path[40:]
	
	
#for each in directory
for fileName in images:

	#load image
	pic = Image.open(fileName)

	#get image metadata
	exif_data = get_exif_data(pic)

	#get GPSInfo
	geo = get_lat_lon(exif_data)

        if geo[0] != None:
            f.write("["+publicHtml(repr(fileName)) + ", " + str(geo[0])+ ", " + str(geo[1])+"],")
	

f.write(']')
f.close() # you can omit in most cases as the destructor will call if  
        


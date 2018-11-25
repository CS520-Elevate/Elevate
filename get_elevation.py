"""
ELEVATION PROFILE APP GENERATOR
ideagora geomatics-2018
http://geodose.com
""" 
import urllib.request
import json
import math
#import matplotlib.pyplot as plt

'''
get_elevation takes in decimals for starting point latitude, starting point longitude, ending point latitude,
ending point longitude, and an integer for points of precision. It returns a triple where the first value
is a list of elevation points (in meters) between the start coordinate point and the end coordinate point, 
a decimal representing the distance between the two points in kilometers, and an integer representing the 
total elevationchange between the two coordinate points. The precision value determines how many elevation 
points evenly spaced between the start and end point are returned.
'''
def get_elevation(start_lat, start_long, end_lat, end_long, precision):
#START-END POINT
    P1=[start_lat,start_long]
    P2=[end_lat,end_long]
    
    

#NUMBER OF POINTS
    s=precision
    interval_lat=(P2[0]-P1[0])/s #interval for latitude
    interval_lon=(P2[1]-P1[1])/s #interval for longitude

    #SET A NEW VARIABLE FOR START POINT
    lat0=P1[0]
    lon0=P1[1]

    #LATITUDE AND LONGITUDE LIST
    lat_list=[lat0]
    lon_list=[lon0]

    #GENERATING POINTS
    for i in range(s):
        lat_step=lat0+interval_lat
        lon_step=lon0+interval_lon
        lon0=lon_step
        lat0=lat_step
        lat_list.append(lat_step)
        lon_list.append(lon_step)

    #HAVERSINE FUNCTION
    def haversine(lat1,lon1,lat2,lon2):
        lat1_rad=math.radians(lat1)
        lat2_rad=math.radians(lat2)
        lon1_rad=math.radians(lon1)
        lon2_rad=math.radians(lon2)
        delta_lat=lat2_rad-lat1_rad
        delta_lon=lon2_rad-lon1_rad
        a=math.sqrt((math.sin(delta_lat/2))**2+math.cos(lat1_rad)*math.cos(lat2_rad)*(math.sin(delta_lon/2))**2)
        d=2*6371000*math.asin(a)
        return d

    #DISTANCE CALCULATION
    d_list=[]
    for j in range(len(lat_list)):
        lat_p=lat_list[j]
        lon_p=lon_list[j]
        dp=haversine(lat0,lon0,lat_p,lon_p)/1000 #km
        d_list.append(dp)
    d_list_rev=d_list[::-1] #reverse list


    #CONSTRUCT JSON
    d_ar=[{}]*len(lat_list)
    for i in range(len(lat_list)):
        d_ar[i]={"latitude":lat_list[i],"longitude":lon_list[i]}
    location={"locations":d_ar}
    json_data=json.dumps(location,skipkeys=int).encode('utf8')

    #SEND REQUEST 
    url="https://api.open-elevation.com/api/v1/lookup"
    response = urllib.request.Request(url,json_data,headers={'Content-Type': 'application/json'})
    fp=urllib.request.urlopen(response)

    #RESPONSE PROCESSING
    res_byte=fp.read()
    res_str=res_byte.decode("utf8")
    js_str=json.loads(res_str)
    #print (js_mystr)
    fp.close()

    #GETTING ELEVATION 
    response_len=len(js_str['results'])
    elev_list=[]
    for j in range(response_len):
        elev_list.append(js_str['results'][j]['elevation'])
    #print(elev_list)
    #BASIC STAT INFORMATION
    mean_elev=round((sum(elev_list)/len(elev_list)),3)
    min_elev=min(elev_list)
    max_elev=max(elev_list)
    distance=d_list_rev[-1]

    change = 0
    i = 1

    while i < len(elev_list):        
        change += abs(elev_list[i-1] - elev_list[i])
        i+=1

    return elev_list, distance, change
#print an example
print(get_elevation(20,20,50,50,100))